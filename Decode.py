import time
import zlib
import numpy as np
from system import util
from PIL import Image, ImageFilter, ImageEnhance

###########################
### BEGIN OF PARAMETERS ###

# Block count in width
# Default value: 118
w_blocks = 118

# Block count in height
# Default value: 169
h_blocks = 169

# Gaussian blur level
# Default value: 1
lvl_blur = 1

# Gamma gain level
# Default value: 2
lvl_gamma = 2

###  END OF PARAMETERS  ###
###########################

def init(w_bl, h_bl, blur, gamma):
    input_dir = './In-Image/'
    output_dir = './Out-Data/'
    util.print_header()
    time_init = time.time()
    input_file_name = util.get_input_file(input_dir)
    img = apply_gamma(apply_blur(util.load_image(input_dir + input_file_name, True), blur), gamma)
    ranges = calc_ranges(img.size, w_bl, h_bl)
    export_data(zlib_decompress(int_convert(octal_convert(read_pixels(img, ranges)))), output_dir)
    print(f'Done in {round(time.time() - time_init, 3)}s.')
    util.full_exit(0)

def apply_blur(img, lvl):
    print('[INFO] Applying Gaussian blur...')
    img = img.filter(ImageFilter.GaussianBlur(lvl))
    print('[INFO] Gaussian blur applied!')
    return img

def apply_gamma(img, lvl):
    print('[INFO] Applying gamma enhance...')
    converter = ImageEnhance.Color(img)
    img = converter.enhance(lvl)
    print('[INFO] Gamma enhance applied!')
    return img

def calc_ranges(img_size, w_blocks, h_blocks):
    print('[INFO] Calculating block ranges...')
    width, height = img_size
    y_ranges = np.linspace(0, height, h_blocks + 1)
    x_ranges = np.linspace(0, width, w_blocks + 1)
    y_ranges = np.round(y_ranges[:-1] + np.diff(y_ranges) / 2)
    x_ranges = np.round(x_ranges[:-1] + np.diff(x_ranges) / 2)
    print('[INFO] Block ranges calculated!')
    return (x_ranges, y_ranges)

def read_pixels(img, ranges):
    print('[INFO] Reading pixels...')
    pixels = []
    for y in ranges[1]:
        for x in ranges[0]:
            pixels.append(img.getpixel((x, y)))
    print('[INFO] All pixels read!')
    return pixels

def octal_convert(pixels):
    print('[INFO] Converting data to octal...')
    octal = ''
    colors = pixels[:8]
    try:
        for i in range(8, len(pixels) - 8):
            octal = ''.join([octal, str(find_closest(colors, pixels[i]))])
    except:
        print('[ERROR] Octal conversion failed!')
        util.full_exit(1)
    print('[INFO] Data converted!')
    return octal

def int_convert(octal):
    print('[INFO] Converting data to integers...')
    try:
        ints = [int(octal[i:i + 3], 8) for i in range(0, len(octal), 3)]
    except:
        print('[ERROR] Integer conversion failed!')
        util.full_exit(1)
    print('[INFO] Data converted!')
    return ints

def zlib_decompress(ints):
    print('[INFO] Decompressing ZLib...')
    data = b''
    d = zlib.decompressobj()
    try:
        for i in range(len(ints)):
            data = b''.join([data, d.decompress(d.unconsumed_tail + bytes([ints[i]]))])
            if d.eof:
                break
    except:
        print('[ERROR] ZLib decompression failed!')
        util.full_exit(1)
    print('[INFO] Data decompressed!')
    return data

def export_data(data, out_dir):
    print('[INFO] Exporting data...')
    data = data.split(b'/', 1)
    path = out_dir + data[0].decode()
    with open(path, 'wb') as out:
        out.write(data[1])
    print(f'[INFO] File saved: {path}!')

def find_closest(colors, color):
    colors = np.array(colors)
    color = np.array(color)
    distances = np.sqrt(np.sum((colors - color) ** 2, axis=1))
    return np.where(distances == np.amin(distances))[0][0]

if  __name__ == '__main__':
    init(w_blocks, h_blocks, lvl_blur, lvl_gamma)
