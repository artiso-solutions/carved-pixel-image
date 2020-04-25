import numpy as np
import os
from generation_parameters import GenerationParameters
from generate_dxf import generate_dxf_circles, generate_dxf_horizontal_bands, generate_dxf_stick_circles, write_stick_length_file
from helper import chunks

# generation_parameters.target_width = 80
# generation_parameters.target_height = 45
# generation_parameters.mm_per_pixel = 6

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Generate pixel art dxf for input image.')
    parser.add_argument('width', help='the width of the image in mm', type=int)
    parser.add_argument('height', help='the height of the image in mm', type=int)
    parser.add_argument('mm_per_pixel', help='the size of one pixel in mm', type=int)
    parser.add_argument('input_files', metavar='image', nargs='+', help='input images for processing')
    parser.add_argument('--show', action='store_true', help='should show generated pixelated image (default false)')
    parser.add_argument('--imgsave', action='store_true', help='save intermediate images (default false)')
    parser.add_argument('--nodxf', action='store_true', help='do not generate dxf file (default false)')
    parser.add_argument('--stick_radius', help='the size of one stick in mm', type=int, default=0)
    parser.add_argument('--stick_min_length', help='the length of a stick representing black value in mm', type=int, default=25)
    parser.add_argument('--stick_usage_length', help='the variable part of stick length in mm', type=int, default=30)
    parser.add_argument('--stick_length_jig_offset', help='the offset of the stick length in mm for your jig', type=int, default=0)

    args = parser.parse_args()
    generation_parameters = GenerationParameters(int(args.width / args.mm_per_pixel), int(args.height / args.mm_per_pixel), args.mm_per_pixel)

    for input_file in args.input_files:
        output_file_circle = f'{os.path.splitext(input_file)[0]}_circle.dxf'
        output_file_horizontal_band = f'{os.path.splitext(input_file)[0]}_horizontal_band.dxf'
        output_file_sticks = f'{os.path.splitext(input_file)[0]}_sticks.dxf'
        output_file_stick_lengths = f'{os.path.splitext(input_file)[0]}_sticks.txt'
        print(f'generating pixel art on input image {input_file} writing output dxf files')

        (img_original, img_grayscale, img_pixelated) = prepare_images(input_file, args.imgsave, generation_parameters)
      
        circles = calculate_circles(img_pixelated, generation_parameters)
        sticks = calculate_sticks(img_pixelated, args.mm_per_pixel, generation_parameters, args.stick_radius, args.stick_min_length, args.stick_usage_length, args.stick_length_jig_offset)

        if not args.nodxf:
            generate_dxf_circles(circles, output_file_circle, generation_parameters)
            generate_dxf_horizontal_bands(circles, output_file_horizontal_band, generation_parameters)
            generate_dxf_stick_circles(sticks, output_file_sticks, generation_parameters)
            write_stick_length_file(sticks, output_file_stick_lengths)

        if args.show == True:
            show_output_images(img_original, img_grayscale, img_pixelated, circles, generation_parameters)

def calculate_circles(pixel_values, generation_parameters):
    print('calculate one circle for each pixel...')
    circles = []
    for y in range(generation_parameters.target_height):
        for x in range(generation_parameters.target_width):
            center = (x * generation_parameters.mm_per_pixel + generation_parameters.mm_per_pixel / 2, generation_parameters.target_height * generation_parameters.mm_per_pixel - y * generation_parameters.mm_per_pixel - generation_parameters.mm_per_pixel / 2)
            gray_value = pixel_values[y, x]
            radius = (1 - gray_value) * generation_parameters.mm_per_pixel / 2
            circles.append((center, radius))
    print(f' - calculated {len(circles)} circles')
    return circles

def calculate_sticks(pixel_values, radius, generation_parameters, stick_radius, stick_min_length, stick_usage_length, stick_length_jig_offset):
    print('calculate one stick for each pixel...')
    sticks = []
    total_length = 0

    radius = generation_parameters.mm_per_pixel
    if stick_radius > 0:
        radius = stick_radius
    
    for y in range(generation_parameters.target_height):
        for x in range(generation_parameters.target_width):
            center = (x * generation_parameters.mm_per_pixel + generation_parameters.mm_per_pixel / 2, generation_parameters.target_height * generation_parameters.mm_per_pixel - y * generation_parameters.mm_per_pixel - generation_parameters.mm_per_pixel / 2)
            gray_value = pixel_values[y, x]
            length = stick_min_length + (1 - gray_value) * stick_usage_length
            sticks.append((center, radius, length - stick_length_jig_offset))
            total_length += length
    print(f' - calculated {len(sticks)} stick lengths with total length of {total_length} mm')
    return sticks

def plot_circles(ax, circles, generation_parameters):
    from matplotlib.patches import Circle
    for (center, radius) in circles:
        circle = Circle(center, radius)
        circle.fill = False
        ax.add_artist(circle)

    ax.set_xlim(0, generation_parameters.target_width * generation_parameters.mm_per_pixel)
    ax.set_ylim(0, generation_parameters.target_height * generation_parameters.mm_per_pixel)
    ax.set_title('Circles')
    ax.set_aspect(1.0)

def plot_horizontal_band(ax, circles, generation_parameters):
    from scipy import interpolate

    points = [(center[0], center[1] + radius*0.8) for (center, radius) in circles]
    point_rows = chunks(points, generation_parameters.target_width)

    for point_row in point_rows:
        point_data = np.array(point_row)
        tck,u = interpolate.splprep(point_data.transpose(), s=0)
        unew = np.arange(0, 1.01, 0.01)
        out = interpolate.splev(unew, tck)

        ax.plot(out[0], out[1], color='black')

    points = [(center[0], center[1] - radius*0.8) for (center, radius) in circles]
    point_rows = chunks(points, generation_parameters.target_width)

    for point_row in point_rows:
        point_data = np.array(point_row)
        tck,u = interpolate.splprep(point_data.transpose(), s=0)
        unew = np.arange(0, 1.01, 0.01)
        out = interpolate.splev(unew, tck)

        ax.plot(out[0], out[1], color='black')

    ax.set_xlim(0, generation_parameters.target_width * generation_parameters.mm_per_pixel)
    ax.set_ylim(0, generation_parameters.target_height * generation_parameters.mm_per_pixel)
    ax.set_title('Horizontal Bands')
    ax.set_aspect(1.0)

def show_output_images(img_original, img_grayscale, img_pixelated, circles, generation_parameters):
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

    plot_circles(ax[4], circles, generation_parameters)
    plot_horizontal_band(ax[5], circles, generation_parameters)

    fig.tight_layout()
    plt.show()

def prepare_images(input_file_path, save_temp_images, generation_parameters):
    from skimage import io
    from skimage import data
    from skimage.color import rgb2gray
    from skimage.transform import resize

    print('preparing images...')
    print(f' - read original image from {input_file_path}')
    img_original = io.imread(input_file_path)
    print(' - transform to grayscale')
    img_grayscale = rgb2gray(img_original)
    print(f' - resize from {img_original.shape[1]}x{img_original.shape[0]} to {generation_parameters.target_width}x{generation_parameters.target_height}')
    img_pixelated = resize(img_grayscale, (generation_parameters.target_height, generation_parameters.target_width))
    

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