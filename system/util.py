import os
import cv2
from PIL import Image

VERSION = '1.0.0'

def print_header():
    print(f'PaperFile v{VERSION} by MasterDevX')
    print('------------------------------')

def get_input_file(input_dir):
    print('[INFO] Looking for input file...')
    file_list = os.listdir(input_dir)
    if len(file_list) < 1:
        print('[ERROR] No input file found!')
        full_exit(1)
    if len(file_list) > 1:
        print('[ERROR] Input directory should contain only one file!')
        full_exit(1)
    file_name = file_list[0]
    print(f'[INFO] Input file found: {input_dir}{file_name}!')
    return file_name

def load_image(img_path, use_pil):
    print('[INFO] Loading input image...')
    try:
        if use_pil:
            img = Image.open(img_path).convert('RGB')
        else:
            img = cv2.imread(img_path)
    except:
        print('[ERROR] Failed to load image!')
        full_exit(1)
    print('[INFO] Image loaded!')
    return img

def export_image(path, img, use_pil):
    print('[INFO] Exporting image...')
    if use_pil:
        img.save(path, 'PNG')
        img.close()
    else:
        cv2.imwrite(path, img)
    print(f'[INFO] Image saved: {path}!')

def full_exit(status_code):
    print()
    input('Press Enter to exit... ')
    exit(status_code)
