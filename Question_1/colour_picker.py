import json
import argparse
import cv2 as cv
import numpy as np


def load_palette(palette_path):
    with open(palette_path, 'r') as file:
        palette_data = json.load(file)
    
    palette = {} # Convert the palette data to a dictionary of color names to RGB values
    for item in palette_data['colour_palette']:
        color_name = item['Colour']
        rgb_value = [int(x) for x in item['RGBValue'].split(',')]
        palette[color_name] = rgb_value
    #print(palette)
    return palette


def closest_color(pixel, palette):
    pixel = np.array(pixel)
    color_names = []
    color_values = []

    for color_name, color_value in palette.items():
        color_names.append(color_name)
        color_values.append(color_value)

    color_values = np.array(color_values)
    distances = np.linalg.norm(color_values - pixel, axis=1)
    closest_index = np.argmin(distances)
    return color_names[closest_index]


def main(image_path, palette_path):
    palette = load_palette(palette_path)

    # Load image
    img = cv.imread(image_path)

    if img is None:
        print(f"Error: Unable to load image at {image_path}")
        return
    
    rows, columns, _ = img.shape
    
    color_count = {color_name: 0 for color_name in palette}

    for i in range(rows):
        for j in range(columns):
            pixel = img[i, j]
            pixel_rgb = [pixel[2], pixel[1], pixel[0]] # convert it to RGB color format
            closest_match = closest_color(pixel_rgb, palette)
            color_count[closest_match] += 1

    
    total_pixels = rows * columns # Calculate the percentage of each color
    color_percentage = {color: (count / total_pixels) * 100 for color, count in color_count.items()}

    result = ", ".join(f"{color}: {percentage:.2f}%" for color, percentage in color_percentage.items())
    print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate colour percentages in an image based on a palette.')
    parser.add_argument('-i', '--image_path', type=str, help='Path to the image file.')
    parser.add_argument('-p', '--palette_path', type=str, help='Path to the palette JSON file.', default="colour_palette.json")
    args = parser.parse_args()

    print("Start processing image with path:", args.image_path)
    main(args.image_path, args.palette_path)
