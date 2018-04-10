import os
from PIL import Image
import argparse

path = "C:/Users/Laurent Berder/Desktop/CRANG/Test_images/"


def downsize_all(args):
    for file in [f for f in os.listdir(args.folder) if '.jpg' in f]:
        im = Image.open(path+file)
        width, height = im.size
        if width > args.max_size or height > args.max_size:
            larger = 'width' if width == max(width, height) else 'height'
            smaller = 'height' if larger == 'width' else 'width'
            ratio = vars()[larger] / vars()[smaller]
            if larger == 'width':
                im.thumbnail((args.max_size, int(args.max_size / ratio)))
            else:
                im.thumbnail((int(args.max_size / ratio), args.max_size))
            im.save(path+file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', help='Which folder to scan')
    parser.add_argument('--max_size', help='Maximum width or height in pixels')
    args = parser.parse_args()
    downsize_all(args)

