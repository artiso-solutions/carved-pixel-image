import numpy as np
import os
from generate_dxf import generate_dxf_circles, generate_dxf_horizontal_bands, generate_dxf_stick_circles, write_stick_length_file
from helper import chunks
from configuration import load_configuration, Configuration, StickConfiguration, Margin

# configuration.width = 80
# generation_parameters.target_height = 45
# configuration.mmPerPixel = 6

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Generate pixel art dxf for input image.')
    parser.add_argument('configuration_file', metavar='config', help='configurations for processing')
    parser.add_argument('input_files', metavar='image', nargs='+', help='input images for processing')
    parser.add_argument('--show', action='store_true', help='should show generated pixelated image (default false)')
    parser.add_argument('--imgsave', action='store_true', help='save intermediate images (default false)')
    parser.add_argument('--nodxf', action='store_true', help='do not generate dxf file (default false)')

    args = parser.parse_args()

    configurations = load_configuration(args.configuration_file)
    for configuration in configurations:
        variant = configuration.variant
        print(f'### using configuration {variant} producing {configuration.width} x {configuration.height} pixels with pixel size {configuration.mmPerPixel}mm ###')
        for input_file in args.input_files:
            output_file = f'{os.path.splitext(input_file)[0]}_{variant}.dxf'
            print(f'generating pixel art on input image {input_file} writing output dxf file')

            (img_original, img_grayscale, img_pixelated) = prepare_images(input_file, args.imgsave, configuration)
        

            if variant == 'circle':
                circles = calculate_circles(img_pixelated, configuration)
                if not args.nodxf:
                    generate_dxf_circles(circles, output_file, configuration)

                if args.show == True:
                    show_output_images(img_original, img_grayscale, img_pixelated, circles, configuration)
            
            if variant == 'band':
                circles = calculate_circles(img_pixelated, configuration)
                if not args.nodxf:
                    generate_dxf_horizontal_bands(circles, output_file, configuration)

                if args.show == True:
                    show_output_images(img_original, img_grayscale, img_pixelated, circles, configuration)

            if variant == 'stick':
                sticks = calculate_sticks(img_pixelated, configuration)
                if not args.nodxf:
                    output_file_stick_lengths = f'{os.path.splitext(input_file)[0]}_stick.txt'
                    generate_dxf_stick_circles(sticks, output_file, configuration)
                    write_stick_length_file(sticks, output_file_stick_lengths)
                # if args.show == True:
                #     show_output_images(img_original, img_grayscale, img_pixelated, circles, configuration)
        
        print()

def pixel_offset(v, offset):
    return v + offset

def calculate_circles(pixel_values, configuration):
    print('calculate one circle for each pixel...')
    circles = []

    total_height = configuration.height * configuration.mmPerPixel + configuration.margin.height

    for y in range(configuration.height):
        for x in range(configuration.width):
            center = (
                pixel_offset(x * configuration.mmPerPixel + configuration.mmPerPixel / 2, configuration.margin.width), 
                total_height - y * configuration.mmPerPixel - configuration.mmPerPixel / 2
            )
            gray_value = pixel_values[y, x]
            radius = (1 - gray_value) * configuration.mmPerPixel / 2
            circles.append((center, radius))
    print(f' - calculated {len(circles)} circles')
    return circles

def calculate_sticks(pixel_values, configuration):
    print('calculate one stick for each pixel...')
    sticks = []
    total_stick_length = 0

    total_height = configuration.height * configuration.mmPerPixel + configuration.margin.height

    radius = configuration.mmPerPixel
    stick_configuration = configuration.stick
    radius = configuration.mmPerPixel

    if stick_configuration.radius > 0:
        radius = stick_configuration.radius
    
    for y in range(configuration.height):
        for x in range(configuration.width):
            center = (
                pixel_offset(x * configuration.mmPerPixel + configuration.mmPerPixel / 2, configuration.margin.width), 
                total_height - y * configuration.mmPerPixel - configuration.mmPerPixel / 2
            )
            gray_value = pixel_values[y, x]
            length = stick_configuration.minLength + (1 - gray_value) * stick_configuration.usageLength
            sticks.append((center, radius, length - stick_configuration.lengthJigOffset))
            total_stick_length += length
    print(f' - calculated {len(sticks)} stick lengths with total length of {total_stick_length} mm')
    return sticks

def plot_circles(ax, circles, configuration):
    from matplotlib.patches import Circle
    for (center, radius) in circles:
        circle = Circle(center, radius)
        circle.fill = False
        ax.add_artist(circle)

    ax.set_xlim(0, configuration.width * configuration.mmPerPixel)
    ax.set_ylim(0, configuration.height * configuration.mmPerPixel)
    ax.set_title('Circles')
    ax.set_aspect(1.0)

def plot_horizontal_band(ax, circles, configuration):
    from scipy import interpolate

    points = [(center[0], center[1] + radius*0.8) for (center, radius) in circles]
    point_rows = chunks(points, configuration.width)

    for point_row in point_rows:
        point_data = np.array(point_row)
        tck,u = interpolate.splprep(point_data.transpose(), s=0)
        unew = np.arange(0, 1.01, 0.01)
        out = interpolate.splev(unew, tck)

        ax.plot(out[0], out[1], color='black')

    points = [(center[0], center[1] - radius*0.8) for (center, radius) in circles]
    point_rows = chunks(points, configuration.width)

    for point_row in point_rows:
        point_data = np.array(point_row)
        tck,u = interpolate.splprep(point_data.transpose(), s=0)
        unew = np.arange(0, 1.01, 0.01)
        out = interpolate.splev(unew, tck)

        ax.plot(out[0], out[1], color='black')

    ax.set_xlim(0, configuration.width * configuration.mmPerPixel)
    ax.set_ylim(0, configuration.height * configuration.mmPerPixel)
    ax.set_title('Horizontal Bands')
    ax.set_aspect(1.0)

def show_output_images(img_original, img_grayscale, img_pixelated, circles, configuration):
    import matplotlib.pyplot as plt

    print('show images')
    fig, axes = plt.subplots(3, 2, figsize=(16, 9))
    ax = axes.ravel()

    ax[0].imshow(img_original)
    ax[0].set_title("Original")
    ax[1].imshow(img_grayscale, cmap=plt.cm.gray)
    ax[1].set_title("Grayscale")
    ax[2].imshow(img_pixelated, cmap=plt.cm.gray)
    ax[2].set_title("Pixelated")
    ax[3].hist(img_pixelated.ravel(), bins=256, range=(0.0, 1.0), fc='k', ec='k')
    ax[3].set_title("Histogram Pixelated")

    plot_circles(ax[4], circles, configuration)
    plot_horizontal_band(ax[5], circles, configuration)

    fig.tight_layout()
    plt.show()

def prepare_images(input_file_path, save_temp_images, configuration):
    from skimage import io
    from skimage import data
    from skimage.color import rgb2gray
    from skimage.transform import resize

    print('preparing images...')
    print(f' - read original image from {input_file_path}')
    img_original = io.imread(input_file_path)
    print(' - transform to grayscale')
    img_grayscale = rgb2gray(img_original)
    print(f' - resize from {img_original.shape[1]}x{img_original.shape[0]} to {configuration.width}x{configuration.height}')
    img_pixelated = resize(img_grayscale, (configuration.height, configuration.width))
    

    if save_temp_images:
        input_image_parts = os.path.splitext(input_file_path)
        temp_output_base_path = f'{input_image_parts[0]}'
        temp_output_base_extension = f'{input_image_parts[1]}'

        grayscale_imge_file_path = f'{temp_output_base_path}_grayscale{temp_output_base_extension}'
        pixelated_imge_file_path = f'{temp_output_base_path}_pixelated{temp_output_base_extension}'
        io.imsave(grayscale_imge_file_path, img_grayscale)
        print(f' - saved intermediate grayscale image to {grayscale_imge_file_path}')
        io.imsave(pixelated_imge_file_path, img_pixelated)
        print(f' - saved pixelated image to {pixelated_imge_file_path}')

    print('images prepared')

    return (img_original, img_grayscale, img_pixelated)


if __name__ == "__main__":
    main()