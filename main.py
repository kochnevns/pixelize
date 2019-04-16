from PIL import Image  
import random
from time import sleep
import sys
import numpy as np  
from os import path

img = Image.open(sys.argv[1], 'r')  


def get_vga_colors():
    colors = []
    for i in range(0, 255):
        red = int(i >> 5) * 32
        green = int((i & 28) >> 2) * 32
        blue = int(i & 3) * 64
        colors.append((red, green, blue))
    return colors

def get_closest_vga(color, vgas):
    dcolors = {}
    for vga_color in vgas:
        dr = abs(color[0] - vga_color[0])
        dg = abs(color[1] - vga_color[1])
        db = abs(color[2] - vga_color[2])
        dcolors[vga_color] = abs(dr + dg + db)
    
    mindcolor = 3131231231231
    closest = None
    for key, value in dcolors.items():
        if value < mindcolor:
            mindcolor = value
            closest = key
    return closest





def get_next_square_of_pixels(x_pos, y_pos, pixel_size, pixels):
    square = []
    try:
        for i in range(x_pos, x_pos + pixel_size):
            for j in range(y_pos, y_pos + pixel_size):
                square.append(pixels[i][j])
    except:
        return []


    return square

def calc_average_color(pixels_list, vgas):
    multiplier = len(pixels_list)
    r,g,b = 0,0,0
    for pixel in pixels_list:
        r += pixel[0]
        g += pixel[1]
        b += pixel[2]

    return get_closest_vga(tuple(map(lambda x: int(x/multiplier), [r,g,b])), vgas)

def loop():
    pixels = np.array(img)
    vgas = get_vga_colors()
    img_x = len(pixels[0])
    img_y = len(pixels)

    pixel_size = 5

    new_pixels = []
    for i in range(0, img_y):
        new_pixels.append([])

    x_pos, y_pos = 0,0

    while(x_pos < img_x and y_pos < img_y):
        square = get_next_square_of_pixels(x_pos, y_pos, pixel_size, pixels)
        if (len(square)):
            pixel_color = calc_average_color(square, vgas)
            for i in range(x_pos, x_pos + pixel_size):
                for j in range(y_pos, y_pos + pixel_size):
                    new_pixels[i].append(pixel_color)

        x_pos += pixel_size
        if (x_pos >= img_x):
            x_pos = 0
            y_pos+= pixel_size
    # Convert the pixels into an array using numpy
    array = np.array(new_pixels, dtype=np.uint8)

    # Use PIL to create an image from the new array of pixels
    new_image = Image.fromarray(array)
    new_image.save('./public/keklol' + sys.argv[1].replace('./uploads/', ''))
    print('new image saved')

loop()
