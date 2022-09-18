# Image manipulation tool to split image into tiles
# python ~/scripts/splitter.py --path__Path --t_size__Tile_size --out__Output_path

import os
from shutil import rmtree
from PIL import Image
import argparse
from PIL import Image
import sys

Image.MAX_IMAGE_PIXELS = 933120000

parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str, required=True)
parser.add_argument('--t_size', type=str, required=True)
parser.add_argument('--out', type=str, required=True)
args = parser.parse_args()

rich_printing = True
try:
    from rich.console import Console
    from rich import print
    from rich.text import Text
    from rich.panel import Panel
except ImportError:
    rich_printing = False

platform_path = '/'
if sys.platform =='win32':
    platform_path = '\\'

image_path = args.path[:-1] if args.path.endswith(platform_path) else args.path
out_path = args.out[:-1] if args.out.endswith(platform_path) else args.out

tile_size = args.t_size
tile_size_x = 0
tile_size_y = 0
if 'x' in tile_size:
    tile_splitted = tile_size.lower().split('x')
    tile_size_x = int(tile_splitted[0])
    tile_size_y = int(tile_splitted[1])
else:
    tile_size_x = int(tile_size)
    tile_size_y = int(tile_size)

image_extensions = [
    '.jpg',
    '.jpeg',
    '.tif',
    '.bmp',
    '.png',
]


def check_image_file(image):
    for image_ext in image_extensions:
        if image.endswith(image_ext):
            return True
    return False


images = [image_path + platform_path + image for image in os.listdir(image_path) if check_image_file(
    image)] if os.path.isdir(image_path) else [image_path]


def print_image_info(image_name, image_ext, width, height, tile_size_x, tile_size_y):
    # Image info
    print(f"Image Name: {image_name}.{image_ext}")
    print(f"Width: {width}")
    print(f"Height: {height}")
    print(f'Extension: {image_ext}')
    print(f"Tile size: {tile_size_x}x{tile_size_y}")


def print_rich_image_info(image_name, image_ext, width, height, tile_size_x, tile_size_y):
    # Image info
    console = Console()

    # title of image panel
    panel_title_text = Text()
    panel_title_text.append("SPLIT", style='green')

    # image name
    image_name_text = Text()
    image_name_text.append("Image Name: ")
    image_name_text.append(image_name + f'.{image_ext}', style='blue')

    print(Panel.fit(image_name_text, style='bold', title=panel_title_text))
    text = Text()
    text.append("Width: ")
    text.append(f"{width}\n", style='bold blue')
    text.append("Height: ")
    text.append(f"{height}\n", style='bold blue')
    text.append("Extension: ")
    text.append(f"{image_ext}\n", style='bold blue')
    text.append("Tile size: ")
    text.append(f"{tile_size_x}x{tile_size_y}\n", style='bold blue')
    console.print(text)


def split_image(image_path):
    if os.path.exists(out_path) == False:
        os.mkdir(out_path)

    out_folder_path = out_path + platform_path + \
        image_path.split(platform_path)[-1].replace('.' +
                                          image_path.split('.')[-1], '_tiled')
    if os.path.exists(out_folder_path):
        rmtree(out_folder_path)

    os.mkdir(out_folder_path)

    image = Image.open(image_path)
    width, height = image.size
    image_name = image_path.split(platform_path)[-1].replace('.' +
                                                   image_path.split('.')[-1], '')
    image_ext = image_path.split('.')[-1]

    if rich_printing:
        print_rich_image_info(image_name, image_ext, width,
                              height, tile_size_x, tile_size_y)
    else:
        print_image_info(image_name, image_ext, width,
                         height, tile_size_x, tile_size_y)

    top = 0
    bottom = tile_size_y
    right = tile_size_x
    left = 0

    # creating tiles
    while True:
        image_tile = image.crop((left, top, right, bottom))
        image_tile.save(out_folder_path + f'/{image_name}_{top}_{left}.{image_ext}')
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


for image in images:
    try:
        split_image(image)
        if rich_printing:
            console = Console()
            text = Text()
            text.append("\n< Done >\n", style="bold green")
            console.print(text)
        else:
            print('\nDone\n')

    except Exception as err:
        if rich_printing:
            console = Console()
            text = Text()
            text.append(f"Error: ", style="bold red")
            text.append(f"{err}\n", style="bold white")
            console.print(text)
        else:
            print(f'Error: {err}')
