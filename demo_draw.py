"""
Homework 3 reborn
Author: Vuong Kha Sieu & Dinh Gia Han
Date: 5/12/2020
Time spent: too much by now
"""
from csc121.image import get_channel, write_jpg
import os, random
import numpy as np
MARGIN = 38 # The radius of a color sphere
BLACK_LEVEL = 242 # Threshold for considering a pixel "black"

def all_colors(filename):
    """
    Creates lists of all RGB pixels of an image by flattening
    the nested lists of RGB pixels 

    Parameters:
        - filename: name of the image
    Returns:
        - red_all, green_all, blue_all: flattened lists of RGB pixels
    """
    red = get_channel(filename, 'red')
    green = get_channel(filename, 'green')
    blue = get_channel(filename, 'blue')
    red_all = []
    blue_all = []
    green_all = []
    height = len(red)
    for row in range(height):
        red_all += red[row]
        blue_all += blue[row]
        green_all += green[row]
    return red_all, green_all, blue_all


def statistic_object_types(red, green, blue):
    """
    Defines groups of colors of an image (color spheres). Each group contains
    colors that are not significantly different from the others

    For example: two colors that have RGB values of (43,128,17) and (50,120,23)
    will likely to be grouped together
    
    Parameters:
        - red, green, blue: flat lists of RGB pixels
    Returns:
       - red_sphere, green_sphere, blue_sphere: three lists whose each nested
       list (color sphere) is a group of colors that are the same or slightly
       different in their RGB values
    """
    red = np.array(red)
    green = np.array(green)
    blue = np.array(blue)
    red_sphere = []
    green_sphere = []
    blue_sphere = []
    count = 0
    # Grouping all colors whose RGB are not greater or less than the
    # comparative pixel(the first color in the colors' arrays) 38 units
    while len(red) > 0:
        check_similar = np.greater(red, red[0] - MARGIN) & np.less(red, red[0] + MARGIN) & \
                        np.greater(green, green[0] - MARGIN) & np.less(green, green[0] + MARGIN) & \
                        np.greater(blue, blue[0] - MARGIN) & np.less(blue, blue[0] + MARGIN)
        red_sphere.append([])
        green_sphere.append([])
        blue_sphere.append([])
        for i in range(len(check_similar)):
            if check_similar[i]:
                red_sphere[count].append(red[i])
                green_sphere[count].append(green[i])
                blue_sphere[count].append(blue[i])
    # After each iteration, remove the pixels that are already grouped
        will_delete = np.invert(check_similar)
        red = red[will_delete]
        green = green[will_delete]
        blue = blue[will_delete]
        count += 1
    return red_sphere, green_sphere, blue_sphere


def calculate_main_colors(red_sphere, green_sphere, blue_sphere):
    """
    Defines the main colors of the image by averaging the RGB values of its color spheres

    Parameters:
        - red_sphere, green_sphere, blue_sphere: three lists whose each
        nested list (color sphere) is a group of pixels that are the same
        or slightly different in their RGB values
    Returns:
        - red, green, blue: three lists contains the average RGB values of
        all color spheres
        - chances: a list contains the number of pixels in each color sphere
    """
    chances = []
    red = []
    green = []
    blue = []
    for idx in range(len(red_sphere)):
        chances.append(len(red_sphere[idx]))
        r = sum(red_sphere[idx]) / chances[idx]
        g = sum(green_sphere[idx]) / chances[idx]
        b = sum(blue_sphere[idx]) / chances[idx]
        red.append((int(r)))
        green.append(int(g))
        blue.append(int(b))
    return red, green, blue, chances


def all_images_color(count, keyword):
    """
    Defines the main colors of all images in the dataset 

    Parameters:
        - count: the number of directories containing the images of the object
                 extracted from the original images
        - keyword: a string of the object of interest
    Returns:
        - red/green/blue_sphere_final: three lists represent the main groups of colors of
        the dataset, whose each nested list (color sphere) is a group of pixels that are
        the same or slightly different in their RGB values
        - chances: a list contains the number of pixels in each color sphere of the dataset
        - processed_image: the number of images that are successfully treated
    """
    imagepath = os.path.join(os.getcwd(), keyword)
    red_dataset = []
    green_dataset = []
    blue_dataset = []
    processed_image = 0
    # Defines the main colors of each image in the dataset
    # by averanging the RGB values of its color spheres
    for i in range(count):
        path = os.path.join(imagepath, str(i))
        image_list = os.listdir(path=path)
        for image in image_list:
            try:
                red, green, blue = all_colors(os.path.join(path, image))
                red_sphere, green_sphere, blue_sphere = statistic_object_types(red, green, blue)
                red, green, blue, chances = calculate_main_colors(red_sphere, green_sphere, blue_sphere)
    # Define the RGB values of the dataset by synthesizing
    # main RGB values of all images
                red_dataset += red
                green_dataset += green
                blue_dataset += blue
                processed_image += 1
            except:
                continue
    # Defines groups of colors of the dataset (color spheres)
    red_sphere_final, green_sphere_final, blue_sphere_final = statistic_object_types(red_dataset, green_dataset, blue_dataset)
    # Noises filtering: if any color that only belongs to less
    # than 5% of the images then it shall be considered a noise
    chances = []
    noises = processed_image//20
    sphere_index = 0
    while sphere_index < len(red_sphere_final):
        chance = len(red_sphere_final[sphere_index])
        if chance > noises:
            chances.append(chance)
            sphere_index += 1
        else:
            red_sphere_final.pop(sphere_index)
            green_sphere_final.pop(sphere_index)
            blue_sphere_final.pop(sphere_index)
    return red_sphere_final, green_sphere_final, blue_sphere_final, chances, processed_image


def demo_draw(filename, red, green, blue, chances, processed_image):
    """
    Colors a black and white sample object.

    Parameters:
        - filename: the image that has the object in black and white
        
        - red, green, blue: three lists represent the main groups of colors of
        the dataset, whose each nested list (color sphere) is a group of colors
        that are the same or slightly different in their RGB values
        
        - chances: a list contains the number of pixels in each color sphere of the dataset;
                   the higher the chance of a group is, the higher probability it gets chosen
                   for coloring
                   
        - processed_image: the number of images that are successfully treated 
    """
    red_channel = get_channel(filename, 'red')
    green_channel = get_channel(filename, 'green')
    blue_channel = get_channel(filename, 'blue')

    height = len(red_channel)
    width = len(red_channel[0])

    # Calculate how many color spheres should be used in the drawing.
    # If the number of images is greater than 100, use only 20 spheres, otherwise,
    # use amount of spheres that is equal to 1/5 of the images.
    if processed_image > 100:
        processed_image = 20
    elif processed_image < 5:
        print("Sorry, there is not enough samples left to draw an image after processing.")
        print("Please delete the dataset and try again with a greater dataset size.")
        return
    else:
        processed_image = processed_image//5

    sphere_color = random.choices(range(len(red)), weights=chances, k=processed_image)

    for row in range(height):
        for col in range(width):
            if red_channel[row][col] < BLACK_LEVEL and \
                    green_channel[row][col] < BLACK_LEVEL and blue_channel[row][col] < BLACK_LEVEL:
                # Randomly choose a group of colors
                sphere_color2 = random.choice(sphere_color)
                # Randomly choose a color in the group of colors at the idx of sphere_color2
                chosen_color = random.choice(range(len(red[sphere_color2])))
                # Color the pixel with the color chosen
                red_channel[row][col] = int(red[sphere_color2][chosen_color])
                green_channel[row][col] = int(green[sphere_color2][chosen_color])
                blue_channel[row][col] = int(blue[sphere_color2][chosen_color])
    write_jpg(red_channel, green_channel, blue_channel, "Computer_draw_" + filename)
