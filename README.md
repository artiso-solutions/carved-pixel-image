# carved-pixel-image
Python helper to generate a pixelated image from a source image and then generates a dxf file with one circle per pixel for carving on a cnc router. Teh idea is to have one circle representing the pixel value via with the diameter of the circle. This way one can use the dxf to create a toolpath for carving on a CNC Router in any material.

# Source Image
A good source image has not too much of details, as it is important to downsample the image. Also the contrast has to be pretty high for good results. One example of an image might be a logo or a portrait. For testing we used our artiso logo changed in the colors and added a simple gradient background:

<img src="documentation/artiso.png" alt="Source image - artiso logo" width="500"/>

## Resolution
To pixelate the image the resolution of the image should be something common and also the aspect ratio shold be reasonable. For testing we resiyed the image to an aspect ration of 16:9 and also decided how our target resolution should be. We used a target resolution of 80 pixel width and 45 pixel width. Therefore we have chosen a multitude of this resolution for the source image.

## Contrast and colors
The image will be converted to grayscale. In the current version there is no adaption of the contrast or pixel values in the code. That is why one has to play with the source image to optimize the result.

To test the source image one can define the commanline option `--imgsave` to save the grayscale and pixelated image to disk in the same directory as the source image. This can help to optimize the source image in multiple iterations. The pixelated image of the artiso logo looks like this:

<img src="documentation/artiso_pixelated.png" alt="Grayscale pixelated image - artiso logo" width="500"/>


# DXF Generation
<img src="documentation/generated-pixel-dxf-artiso-logo.png" alt="Generated DXF with Circles - artiso logo" width="500"/>

# Producing Art
<img src="documentation/artiso-logo-production-mpcnc.jpg" alt="Progress during production on MPCNC - artiso logo" width="500"/>

<img src="documentation/artiso-logo-plywood.jpg" alt="Finished result carved in plywood - artiso logo" width="500"/>


<img src="documentation/artiso-logo-plywood-details.jpg" alt="Detail shot on carved result - artiso logo" width="500"/>

# Tweaking the output

# Future Optimization
