import time
import zlib
import math
from system import util
from PIL import Image, ImageDraw, ImageFont

###########################
### BEGIN OF PARAMETERS ###

# Sheet height in pixels
# Default value: 3508
paper_height_px = 3508

# Sheet width in pixels
# Default value: 2480
paper_width_px = 2480

# Margin size in pixels
# Default value: 59
margin_px = 59

# Block side size in pixels
# Default value: 20
block_size_px = 20

###  END OF PARAMETERS  ###
###########################

def init(margin, block_size, width, height):
    font_path = './system/font.ttf'
    input_dir = './In-Data/'
    output_dir = './Out-Image/'
    util.print_header()
    time_init = time.time()
    input_file_name = util.get_input_file(input_dir)
    data = read_file(input_dir + input_file_name)
    raw_size = len(data)
    data = external_hdr(octal_convert(zlib_compress(internal_hdr(input_file_name, data))))
    w_cap, h_cap = get_capacity(len(data), block_size, margin, width, height)
    img, draw = make_image(width, height)
    put_label(font_path, draw, width, w_cap, margin, raw_size, len(data), block_size)
    draw_grid(draw, margin, width, block_size, len(data))
    draw_blocks(draw, block_size, margin, w_cap, h_cap, data)
    util.export_image(output_dir + input_file_name + '.png', img, True)
    print(f'Done in {round(time.time() - time_init, 3)}s.')
    util.full_exit(0)

def read_file(file_path):
    print('[INFO] Reading data from file...')
    with open(file_path, 'rb') as file:
        data = file.read()
    if len(data) == 0:
        print('[ERROR] Input file does not contain any data!')
        util.full_exit(1)
    print('[INFO] Data loaded!')
    return data

def internal_hdr(file_name, data):
    print('[INFO] Writing internal header...')
    data = b''.join([file_name.encode(), b'/', data])
    print('[INFO] Internal header written!')
    return data

def zlib_compress(data):
    print('[INFO] Compressing data with ZLib...')
    data = zlib.compress(data, 9)
    print('[INFO] Data compressed!')
    return data

def octal_convert(data):
    print('[INFO] Converting data to octal...')
    data = ''.join([oct(i)[2:].zfill(3) for i in data])
    print('[INFO] Data converted!')
    return data

def external_hdr(data):
    print('[INFO] Writing external header...')
    data = ''.join(['01234567', data])
    print('[INFO] External header written!')
    return data

def get_capacity(data_size, block_size, margin, width, height):
    print('[INFO] Calculating grid capacity...')
    h_cap = count_blocks(block_size, margin, height)
    w_cap = count_blocks(block_size, margin, width)
    print('[INFO] Capacity calculated!')
    print('[INFO] Checking if data fits grid capacity...')
    if data_size > h_cap * w_cap:
        print('[ERROR] Data overflow detected!')
        util.full_exit(1)
    print('[INFO] Data size matches grid!')
    return (w_cap, h_cap)

def make_image(width, height):
    print('[INFO] Making image template...')
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    print('[INFO] Image template created!')
    return (img, draw)

def put_label(font_path, draw, width, w_cap, margin, raw_size, data_size, block_size):
    print('[INFO] Putting image label...')
    h_cap = math.ceil(data_size / count_blocks(block_size, margin, width))
    font = ImageFont.truetype(font_path, margin - int(margin / 3))
    cfg_line = f'Capacity: {w_cap}x{h_cap} ({w_cap * h_cap} blocks, {raw_size / 1000} Kb)'
    w_text = draw.textlength(text=cfg_line, font=font)
    draw.text((margin, 0), 'PaperFile data map', (0, 0, 0), font=font)
    draw.text((width - (margin + w_text), 0), cfg_line, (0, 0, 0), font=font)
    print('[INFO] Label put!')

def draw_grid(draw, margin, width, block_size, data_size):
    print('[INFO] Drawing grid...')
    page_edge = get_page_edge(block_size, margin, width)
    data_edge = get_data_edge(block_size, data_size, margin, width)
    fields = {
        0: {
            'edge': width - margin + 1,
            'x2y2': data_edge
        },
        1: {
            'edge': data_edge + 1,
            'x2y2': page_edge
        }
    }
    for i in range(2):
        order = (-1) ** (i + 1)
        for j in range(margin, fields[i]['edge'], block_size):
            x1y1 = (margin, j)[::order]
            x2y2 = (fields[i]['x2y2'], j)[::order]
            draw.line((x1y1, x2y2), fill=(0, 0, 0))
    print('[INFO] Grid drawn!')

def draw_blocks(draw, block_size, margin, w_cap, h_cap, octal):
    print('[INFO] Drawing blocks...')
    colors = [
        (255, 255, 255),    # [0] White,    (R, G, B)
        (0, 0, 0),          # [1] Black,    ()
        (255, 0, 0),        # [2] Red,      (R)
        (0, 255, 0),        # [3] Green,    (G)
        (0, 0, 255),        # [4] Blue,     (B)
        (255, 255, 0),      # [5] Yellow,   (R, G)
        (255, 0, 255),      # [6] Magenta,  (R, B)
        (0, 255, 255)       # [7] Cyan,     (G, B)
    ]
    for y in range(h_cap):
        for x in range(w_cap):
            block_number = y * w_cap + x
            fill = colors[int(octal[block_number])]
            x1y1 = (margin + block_size * x + 1, margin + block_size * y + 1)
            x2y2 = (margin + block_size * (x + 1) - 1, margin + block_size * (y + 1) - 1)
            draw.rectangle((x1y1, x2y2), fill=fill)
            if block_number + 1 == len(octal):
                break
        else:
            continue
        break
    print('[INFO] All blocks drawn!')

def count_blocks(block_size, margin, field):
    return int((field - margin * 2) / block_size)

def get_page_edge(block_size, margin, field):
    return block_size * count_blocks(block_size, margin, field) + margin

def get_data_edge(block_size, data_size, margin, field):
    return block_size * math.ceil(data_size / count_blocks(block_size, margin, field)) + margin

if __name__ == '__main__':
    init(margin_px, block_size_px, paper_width_px, paper_height_px)
