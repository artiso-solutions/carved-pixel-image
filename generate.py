import numpy as np
import os

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

        (img_original, img_grayscale, img_pixelated) = prepare_images(input_file, args.imgsave)
      
        circles = calculate_circles(img_pixelated)

        if not args.nodxf:
            generate_circle_dxf(circles, output_file_circle)
            generate_horizontal_band_dxf(img_pixelated, output_file_horizontal_band)

        if args.show == True:
            show_output_images(img_original, img_grayscale, img_pixelated, circles)

def calculate_circles(pixel_values):
    print('calculate one circle for each pixel...')
    circles = []
    for x in range(TARGET_WIDTH):
        for y in range(TARGET_HEIGHT):
            center = (x * MM_PER_PIXEL + MM_PER_PIXEL / 2, TARGET_HEIGHT * MM_PER_PIXEL - y * MM_PER_PIXEL - MM_PER_PIXEL / 2)
            gray_value = pixel_values[y, x]
            radius = (1 - gray_value) * MM_PER_PIXEL / 2
            circles.append((center, radius))
    print(f' - calculated {len(circles)} circles')
    return circles

def generate_horizontal_band_dxf(pixel_values, output_file_path):
    print('generate horizontal band dxf...')

def generate_circle_dxf(circles, output_file_path):
    import ezdxf

    print('writing dxf output...')
    doc = ezdxf.new(dxfversion='R2010')
    msp = doc.modelspace()

    print(' - draw outer box')
    msp.add_line((0,0), (TARGET_WIDTH * MM_PER_PIXEL,0))
    msp.add_line((TARGET_WIDTH * MM_PER_PIXEL,0), (TARGET_WIDTH * MM_PER_PIXEL, TARGET_HEIGHT * MM_PER_PIXEL))
    msp.add_line((TARGET_WIDTH * MM_PER_PIXEL,TARGET_HEIGHT * MM_PER_PIXEL), (0,TARGET_HEIGHT * MM_PER_PIXEL))
    msp.add_line((0, TARGET_HEIGHT * MM_PER_PIXEL), (0,0))
    print(f' - draw {TARGET_WIDTH * TARGET_HEIGHT} circles with {MM_PER_PIXEL} mm per pixel')

    for circle in circles:
        (center, radius) = circle
        msp.add_circle(center, radius)
        
    print(f'write dxf to {output_file_path}')
    doc.saveas(output_file_path)
    return circles

def show_output_images(img_original, img_grayscale, img_pixelated, circles):
    from matplotlib.patches import Circle
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

    for (center, radius) in circles:
        circle = Circle(center, radius)
        circle.fill = False
        ax[4].add_artist(circle)

    ax[4].set_xlim(0, TARGET_WIDTH * MM_PER_PIXEL)
    ax[4].set_ylim(0, TARGET_HEIGHT * MM_PER_PIXEL)
    ax[4].set_title('Circles')
    ax[4].set_aspect(1.0)

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