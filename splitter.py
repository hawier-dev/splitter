"""
Splitter

Split image into tiles of specified size

Usage:
    python splitter.py --path <image_path> --t_size <tile_size_x>x<tile_size_y> --out <out_path>

Example:
    python splitter.py --path /home/user/image.jpg --t_size 256x256 --out /home/user/tiles
"""

import os
from shutil import rmtree
import argparse
from PIL import Image
import sys

Image.MAX_IMAGE_PIXELS = 933120000


def parse_args():
    parser = argparse.ArgumentParser("Split image into tiles of specified size")
    parser.add_argument("-p", "--path", type=str, required=True, help="Path to image")
    parser.add_argument(
        "-t",
        "--t_size",
        type=str,
        required=True,
        help="Tile size in format <tile_size_x>x<tile_size_y>",
    )
    parser.add_argument("-o", "--out", type=str, required=True, help="Output path")
    args = parser.parse_args()

    if os.path.isdir(args.path):
        files = [
            os.path.join(args.path, file)
            for file in os.listdir(args.path)
            if check_image_file(file)
        ]
    elif check_image_file(args.path):
        files = [args.path]
    else:
        files = []

    if not files:
        print("No images found in specified path")
        sys.exit()

    tile_size = args.t_size.split("x")

    if type(tile_size) == list:
        tile_size_x = int(tile_size[0])
        tile_size_y = int(tile_size[1])

    else:
        tile_size_x = int(tile_size)
        tile_size_y = int(tile_size)

    return files, tile_size_x, tile_size_y, args.out


def check_image_file(image):
    image_extensions = [".jpg", ".jpeg", ".tif", ".bmp", ".png", ".gif"]
    for image_ext in image_extensions:
        if image.endswith(image_ext):
            return True
    return False


def split_image(image_path, out_path, tile_size_x, tile_size_y):
    if not os.path.exists(out_path):
        os.mkdir(out_path)

    out_folder_path = os.path.join(
        out_path, os.path.splitext(os.path.basename(image_path))[0] + "_tiled"
    )
    if os.path.exists(out_folder_path):
        rmtree(out_folder_path)

    os.mkdir(out_folder_path)

    image = Image.open(image_path)
    width, height = image.size
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    image_ext = image_path.split(".")[-1]

    top = 0
    bottom = tile_size_y
    right = tile_size_x
    left = 0

    # creating tiles
    while True:
        image_tile = image.crop((left, top, right, bottom))
        image_tile.save(
            os.path.join(out_folder_path, f"{image_name}_{top}_{left}.{image_ext}")
        )
        if right == width and bottom == height:
            break
        if right == width:
            if bottom + tile_size_y > height:
                bottom = height
                top += tile_size_y
            else:
                bottom += tile_size_y
                top += tile_size_y
            left = 0
            right = tile_size_x
        else:
            if right + tile_size_x > width:
                right = width
                left += tile_size_x
            else:
                right += tile_size_x
                left += tile_size_x


def main():
    files, tile_size_x, tile_size_y, out_path = parse_args()
    for file in files:
        split_image(file, out_path, tile_size_x, tile_size_y)


if __name__ == "__main__":
    main()
