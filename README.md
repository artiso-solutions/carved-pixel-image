# carved-pixel-image
Python helper to generate a pixelated image from a source image and then generates a dxf file with one circle per pixel for carving on a CNC Router. The idea is to have one circle representing the pixel value via with the diameter of the circle. This way one can use the dxf to create a toolpath for carving on a CNC Router in any material.

# Configuration of Art Generation
As there are three variants right now (possibility to add more in future) which also might vary in paramteres, it is the easiest way to introduce a configuration file. In this file one configuraiton for each variant can be defined with different parameters to get the best result for each technique. An example configuration with all parameters can be found in [sample_configuration.json](./sample_configuration.json). The configuration classes with documentation is located in [configuration.py](./configuration.py).

# Source Image
A good source image has not too much of details, as it is important to downsample the image. Also the contrast has to be pretty high for good results. One example of an image might be a logo or a portrait. For testing we used our artiso logo changed in the colors and added a simple gradient background:

<img src="documentation/artiso.png" alt="Source image - artiso logo" width="500"/>

All image handling is done via [scikit-image](https://scikit-image.org/).

## Resolution
To pixelate the image the resolution of the image should be something common and also the aspect ratio shold be reasonable. For testing we resiyed the image to an aspect ration of 16:9 and also decided how our target resolution should be. We used a target resolution of 80 pixel width and 45 pixel width. Therefore we have chosen a multitude of this resolution for the source image.

## Contrast and colors
The image will be converted to grayscale. In the current version there is no adaption of the contrast or pixel values in the code. That is why one has to play with the source image to optimize the result.

To test the source image one can define the commanline option `--imgsave` to save the grayscale and pixelated image to disk in the same directory as the source image. This can help to optimize the source image in multiple iterations. The pixelated image of the artiso logo looks like this:

<img src="documentation/artiso_pixelated.png" alt="Grayscale pixelated image - artiso logo" width="500"/>

# DXF Generation
In order to carve the pixel art with a CNC router we need some way to generate the gcode. As an intermediate step we choose to generate a dxf file with the outline of the carves. For the dxf generation we are using [ezdxf](https://pypi.org/project/ezdxf/). 

Both following variants are generated in based on the same parameters. The dxf files are suffixed with `_circle.dxf` / `_horizontal_band.dxf`.

## One Circle per Pixel
For this variant we are converting the pixel images to a grid of circles. Each pixel is represented by one circle and the radius of this circle is determined by the gray value of the pixel.

<img src="documentation/generated-pixel-dxf-artiso-logo.png" alt="Generated DXF with Circles - artiso logo" width="500"/>

Showing this dxf in a CAM program helps deciding if the source image is well prepared for carving in wood.

## One Carved Horizontal Line for All Pixels in One Row
With the second variant we are converting the pixel image to horizontal bands. Each row of pixels is represented by a band where the width of each pixel is determined by the gray value of the pixel. The bands can then be carved with a router.

<img src="documentation/generated-bands-dxf-artiso-logo.png" alt="Generated DXF with horizontal bands - artiso logo" width="500"/>

## One Stick Per Pixel With Length Based On Pixel Value
The third variant does not use the carving for representing the pixel value but uses sticks with the same diameter but the length depending on the pixel value. Therefore the dxf generation is very easy as one circle per pixel with the correct diameter depending on the stick size has to be generated. In this variant a text file is also generated which contains the information of each stick with its position and its length. Thias file can be output with the `print_stick_length.py` script. This prints one length at a time and one has to proceed by pressing enter. This script saves its current position so one resume at the correct position later. The output looks like the following picture.

<img src="documentation/stick-length.jpg" alt="Output of print_stick_length" width="300"/>

# Producing Art
The generated dxf can be used to create the toolpaths in any CAM program. For the MPCNC we use [Estlcam](https://www.estlcam.de/). It is very easy to import the dxf and let Estlcam autogenerate the carvings. For the artiso logo we chose to use a 90° engraving bit. The processing of the image can take some minutes depending on the number of circles. After generating the carvings for closed paths one can tweek the parameters of the carvings. We decided to limit the depth to 1.5 mm which looks pretty good. Feel free to play around with the parameters to create a good result for your case.

During processing of the gcode it looks very interesting, as the router takes several passes in almost random order. That might be some way for improvement to generate gcoe based on some templates by ourselves and optimize the processing order.

<img src="documentation/artiso-logo-production-mpcnc.jpg" alt="Progress during production on MPCNC - artiso logo" width="500"/>

The result of the artiso logo carved in plywood on our MPCNC after cutting down the plywood (we engraved the bounding box as guide for cutting) looks very pleasent for us. We are happy with the result.

<img src="documentation/artiso-logos-plywood.jpg" alt="Finished result carved in plywood - artiso logo" width="500"/>


<img src="documentation/artiso-logos-plywood-details.jpg" alt="Detail shot on carved result - artiso logo" width="500"/>

The third variant takes a lot of time as 1152 sticks has to be cut and glued in place. Therefore its not yet finished. But it looks promissing even in this state.

<img src="documentation/artiso-logo-sticks-intermediate.jpg" alt="Intermediate result with sticks - artiso logo" width="500"/>

The speed up cutting the sticks in the correct length we created a jig for measuring and cuttong.

<img src="documentation/stick-jig.jpg" alt="Jig for cutting sticks" width="500"/>

# Future Optimization
There are some simple improvements waiting for implementation:
 - [ ] Packaging of library for reuse
 - [ ] Narrow down pixel values for more control over pixel radius
 - [ ] Define image size via commandline
 
 Add more variations:
 - [x] horizontal band per row of pixels
 - [x] one stick per pixel with different length based on pixel value
 - [ ] horinzontal lines with y-axis translation based on pixel value