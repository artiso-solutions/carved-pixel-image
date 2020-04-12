import numpy as np
import os

TARGET_WIDTH = 80
TARGET_HEIGHT = 45
MM_PER_PIXEL = 6

def main():
    inputFile = './artiso.png'
    outputFile = f'{os.path.splitext(inputFile)[0]}.dxf'
    print(f'generating pixel art on input image {inputFile} writing output dxf file to {outputFile}')

    (img_original, img_grayscale, img_pixelated) = prepare_images(inputFile)
    generate_dxf(img_pixelated, outputFile)
    show_output_images(img_original, img_grayscale, img_pixelated)

def generate_dxf(pixel_values, output_file_path):
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
    for x in range(TARGET_WIDTH):
        for y in range(TARGET_HEIGHT):
            center = (x * MM_PER_PIXEL + MM_PER_PIXEL / 2, TARGET_HEIGHT * MM_PER_PIXEL - y * MM_PER_PIXEL - MM_PER_PIXEL / 2)
            gray_value = pixel_values[y, x]
            radius = (1 - gray_value) * MM_PER_PIXEL / 2
            msp.add_circle(center, radius)
    print(f'write dxf to {output_file_path}')
    doc.saveas(output_file_path)

def show_output_images(img_original, img_grayscale, img_pixelated):
    import matplotlib.pyplot as plt

    print('show images')
    fig, axes = plt.subplots(1, 3, figsize=(8, 4))
    ax = axes.ravel()

    ax[0].imshow(img_original)
    ax[0].set_title("Original")
    ax[1].imshow(img_grayscale, cmap=plt.cm.gray)
    ax[1].set_title("Grayscale")
    ax[2].imshow(img_pixelated, cmap=plt.cm.gray)
    ax[2].set_title("Pixelated")

    fig.tight_layout()
    plt.show()

def prepare_images(input_file_path):
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
    print('images prepared')
    return (img_original, img_grayscale, img_pixelated)


if __name__ == "__main__":
    main()