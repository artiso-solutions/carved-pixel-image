import numpy as np
import os
from generation_parameters import GenerationParameters
from generate_dxf import generate_dxf_circles, generate_dxf_horizontal_bands

TARGET_WIDTH = 80
TARGET_HEIGHT = 45
MM_PER_PIXEL = 6

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Generate pixel art dxf for input image.')
    parser.add_argument('input_files', metavar='image', nargs='+', help='input images for processing')
    parser.add_argument('--show', action='store_true', help='should show generated pixelated image (default false)')
    parser.add_argument('--imgsave', action='store_true', help='save intermediate images (default false)')
    parser.add_argument('--nodxf', action='store_true', help='do not generate dxf file (default false)')

    args = parser.parse_args()

    for input_file in args.input_files:
        output_file_circle = f'{os.path.splitext(input_file)[0]}_circle.dxf'
        output_file_horizontal_band = f'{os.path.splitext(input_file)[0]}_horizontal_band.dxf'
        print(f'generating pixel art on input image {input_file} writing output dxf files')

        generation_parameters = GenerationParameters(TARGET_WIDTH, TARGET_HEIGHT, MM_PER_PIXEL)

        (img_original, img_grayscale, img_pixelated) = prepare_images(input_file, args.imgsave)
      
        circles = calculate_circles(img_pixelated)

        if not args.nodxf:
            generate_dxf_circles(circles, output_file_circle, generation_parameters)
            generate_dxf_horizontal_bands(img_pixelated, output_file_horizontal_band)

        if args.show == True:
            show_output_images(img_original, img_grayscale, img_pixelated, circles)

def calculate_circles(pixel_values):
    print('calculate one circle for each pixel...')
    circles = []
    for y in range(TARGET_HEIGHT):
        for x in range(TARGET_WIDTH):
            center = (x * MM_PER_PIXEL + MM_PER_PIXEL / 2, TARGET_HEIGHT * MM_PER_PIXEL - y * MM_PER_PIXEL - MM_PER_PIXEL / 2)
            gray_value = pixel_values[y, x]
            radius = (1 - gray_value) * MM_PER_PIXEL / 2
            circles.append((center, radius))
    print(f' - calculated {len(circles)} circles')
    return circles



def plot_circles(ax, circles):
    from matplotlib.patches import Circle
    for (center, radius) in circles:
        circle = Circle(center, radius)
        circle.fill = False
        ax.add_artist(circle)

    ax.set_xlim(0, TARGET_WIDTH * MM_PER_PIXEL)
    ax.set_ylim(0, TARGET_HEIGHT * MM_PER_PIXEL)
    ax.set_title('Circles')
    ax.set_aspect(1.0)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def plot_horizontal_band(ax, circles):
    from scipy import interpolate

    points = [(center[0], center[1] + radius*0.8) for (center, radius) in circles]
    point_rows = chunks(points, TARGET_WIDTH)

    for point_row in point_rows:
        point_data = np.array(point_row)
        tck,u = interpolate.splprep(point_data.transpose(), s=0)
        unew = np.arange(0, 1.01, 0.01)
        out = interpolate.splev(unew, tck)

        ax.plot(out[0], out[1], color='black')

    points = [(center[0], center[1] - radius*0.8) for (center, radius) in circles]
    point_rows = chunks(points, TARGET_WIDTH)

    for point_row in point_rows:
        point_data = np.array(point_row)
        tck,u = interpolate.splprep(point_data.transpose(), s=0)
        unew = np.arange(0, 1.01, 0.01)
        out = interpolate.splev(unew, tck)

        ax.plot(out[0], out[1], color='black')

    ax.set_xlim(0, TARGET_WIDTH * MM_PER_PIXEL)
    ax.set_ylim(0, TARGET_HEIGHT * MM_PER_PIXEL)
    ax.set_title('Horizontal Bands')
    ax.set_aspect(1.0)

def show_output_images(img_original, img_grayscale, img_pixelated, circles):
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

    plot_circles(ax[4], circles)
    plot_horizontal_band(ax[5], circles)

    fig.tight_layout()
    plt.show()

def prepare_images(input_file_path, save_temp_images):
    from skimage import io
    from skimage import data
    from skimage.color import rgb2gray
    from skimage.transform import resize

    print('preparing images...')
    print(f' - read original image from {input_file_path}')
    img_original = io.imread(input_file_path)
    print(' - transform to grayscale')
    img_grayscale = rgb2gray(img_original)
    print(f' - resize from {img_original.shape[1]}x{img_original.shape[0]} to {TARGET_WIDTH}x{TARGET_HEIGHT}')
    img_pixelated = resize(img_grayscale, (TARGET_HEIGHT, TARGET_WIDTH))
    

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