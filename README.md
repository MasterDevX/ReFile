## ReFile
This is an experimental project that allows to save regular files on plain paper. The project has no practical use because you can only store tiny files with a size up to few tens of kilobytes on a paper sheet, however it demonstrates that the idea actually works and the regular files can be stored in this way.

## Dependencies
Before using ReFile you have to install required modules using pip:
```
pip install Pillow opencv-python numpy 
```

## Project structure
The system consists of three main components, each of them is a python executable script. Some scripts have parameters you can modify by opening a script with any text / code editor. 
- **Encode.py** - File encoder. Looks for input file in **In-Data**, compresses it's data with ZLib and converts it to octal data. Then the image with octal data is being generated. The image uses 8-color palette where each color represent's a number from range 0 - 7 (all possible numbers in octal system). The image is being saved to **Out-Image**.

  Component parameters:
  - **paper_height_px** - height of a paper sheet in pixels you are going to print your encoded image on. The image with a corresponding height will be generated. The default value is 3508 pixels, which represents the height of an A4 sheet at 300 DPI.
  - **paper_width_px** - width of a paper sheet in pixels you are going to print your encoded image on. The image with a corresponding width will be generated. The default value is 2480 pixels, which represents the width of an A4 sheet at 300 DPI.
  - **margin_px** - size of a margin in pixels that will be symmetrically applied on the generated image. Useful for the printers that don't support borderless printing. The default value is 59 pixels which is equal to 0.5 cm at 300 DPI.
  - **block_size_px** - size of a single data block side in pixels. The less value means more data blocks can be placed so bigger files can be stored on the same sheet of paper and vice versa. The default value is 20 pixels which is equal to 1.7 mm at 300 DPI. 

- **Decode.py** - Image decoder. Looks for input image in **In-Image** and decodes it back to the file using the reversed algorithm of the encoder. The output file is saved to **Out-Data**.

  Component parameters:
  - **w_blocks** - number of data blocks placed on the input image horizontally (in width). Should be set to the value printed on the top of the scanned image. The default value is 118 which is the max horizontal block count for default encoder parameters.
  - **h_blocks** - number of data blocks placed on the input image vertically (in height). Should be set to the value printed on the top of the scanned image. The default value is 169 which is the max vertical block count for default encoder parameters.
  - **lvl_blur** - radius of the Gaussian blur to apply to the image during the decoding process internally (will not affect the image on a disk). Usually helps to reduce the noise of the scanned image. Higher value means stronger blur and vice versa. Set to 0 to disable Gaussian blur (not recommended). The default value is 1.
  - **lvl_gamma** - gamma enhance factor to apply to the image during the decoding process internally (will not affect the image on a disk). Usually compensates the saturation loss after a print / scan cycle. Higher value means stronger gamma enhancement and vice versa. May not be required if no saturation loss occurred. Set to 0 to disable gamma enhance. The default value is 2.
 
 - **Crop.py** - Image cropping & perspective transformation tool. Looks for input image in **In-Crop**, runs an interactive point selector, crops the image and transforms the image perspective by four points selected by user and saves modified image to **Out-Crop**.

Folder **system** contains the font [Roboto Mono](https://fonts.google.com/specimen/Roboto+Mono) used to print the image informational header and a script **util.py** that includes some common functions used by all three main components of the project described above.

## Usage
### Encoding process
1. Place the file you want to encode inside **In-Data** directory.
2. Configure the encoder parameters if needed (see [Project structure](#project-structure) for encoder parameters description).
3. Run the encoder using Python interpreter:

    ```
    python3 Encode.py
    ```
    
4. If no errors occurred during the encoding process, you can now grab the generated image from **Out-Image** directory and print it on a paper.

### Decoding process
1. Scan the paper sheet containing the file you want to decode with a scanner (alternatively, take a picture of it with a camera).
2. Place the scanned image inside **In-Crop** directory.
3. Run the cropping & perspective transformation tool using Python interpreter:

    ```
    python3 Crop.py
    ```
 
4. By double-clicking the left mouse button, select top-left, top-right, bottom-left and bottom-right corners of the data grid (the actual order doesn't matter), press Enter when all four points selected. Click the right mouse button on the image to clear the selected points.
5. Grab the modified image from **Out-Crop** and place it inside **In-Image** directory.
6. Configure the decoder parameters if needed (see [Project structure](#project-structure) for decoder parameters description).
7. Run the decoder using Python interpreter:

    ```
    python3 Decode.py
    ```
    
8. If no errors occurred during the decoding process, you can now grab the output file from **Out-Data** directory.
