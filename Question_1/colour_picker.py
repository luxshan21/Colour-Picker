import json
import argparse
# import your module here


def load_palette(palette_path):
    with open(palette_path, 'r') as file:
        palette = json.load(file)
    return palette


def main(image_path, palette_path):
    palette = load_palette(palette_path)
    # load Image

    # use print to output the result in format "color1: percentage1. Color2: percentage2..."


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate color percentages in an image based on a palette.')
    parser.add_argument('-i', '--image_path', type=str, help='Path to the image file.')
    parser.add_argument('-p', '--palette_path', type=str,
                        help='Path to the palette JSON file.', default="color_palette.json")
    args = parser.parse_args()

    print("Start processing image with path:", args.image_path)
    main(args.image_path, args.palette_path)
