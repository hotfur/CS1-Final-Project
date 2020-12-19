"""
Mainframe for Clockwork Artist
Author: Vuong Kha Sieu & Dinh Gia Han
Date: 18/12/2020
"""
import search, detection, demo_draw, os
from csc121 import image

# current directory
curdir = os.getcwd()

# This is a dictionary of object that ImageAi can detect.
obj_dict = {'person': 'invalid', 'bicycle': 'invalid', 'car': 'invalid', 'motorcycle': 'invalid', 'airplane': 'invalid', 'bus': 'invalid', 'train': 'invalid', 'truck': 'invalid',
            'boat': 'invalid', 'traffic light': 'invalid', 'fire hydrant': 'invalid', 'stop sign': 'invalid', 'parking meter': 'invalid', 'bench': 'invalid', 'bird': 'invalid',
            'cat': 'invalid', 'dog': 'invalid', 'horse': 'invalid', 'sheep': 'invalid', 'cow': 'invalid', 'elephant': 'invalid', 'bear': 'invalid', 'zebra': 'invalid',
            'giraffe': 'invalid', 'backpack': 'invalid', 'umbrella': 'invalid', 'handbag': 'invalid', 'tie': 'invalid', 'suitcase': 'invalid', 'frisbee': 'invalid', 'skis':
            'invalid', 'snowboard': 'invalid', 'sports ball': 'invalid', 'kite': 'invalid', 'baseball bat': 'invalid', 'baseball glove': 'invalid', 'skateboard': 'invalid',
            'surfboard': 'invalid', 'tennis racket': 'invalid', 'bottle': 'invalid', 'wine glass': 'invalid', 'cup': 'invalid', 'fork': 'invalid', 'knife': 'invalid',
            'spoon': 'invalid', 'bowl': 'invalid', 'banana': 'invalid', 'apple': 'invalid', 'sandwich': 'invalid', 'orange': 'invalid', 'broccoli': 'invalid', 'carrot': 'invalid',
            'hot dog': 'invalid', 'pizza': 'invalid', 'donut': 'invalid', 'cake': 'invalid', 'chair': 'invalid', 'couch': 'invalid', 'potted plant': 'invalid', 'bed': 'invalid',
            'dining table': 'invalid', 'toilet': 'invalid', 'tv': 'invalid', 'laptop': 'invalid', 'mouse': 'invalid', 'remote': 'invalid', 'keyboard': 'invalid',
            'cell phone': 'invalid', 'microwave': 'invalid', 'oven': 'invalid', 'toaster': 'invalid', 'sink': 'invalid', 'refrigerator': 'invalid', 'book': 'invalid',
            'clock': 'invalid', 'vase': 'invalid', 'scissors': 'invalid', 'teddy bear': 'invalid', 'hair dryer': 'invalid', 'toothbrush': 'invalid'}
# Print out instruction entering the object
print("Firstly, please input the object name that you want to draw")
print("Please be specific in naming, for example, you might want"
      "to name it in form of 'adjective' + 'object name'")
print("And make sure that the object has to be one of these things:")
# Print 10 objects/line for easy-to-read display
i = 0
for obj in obj_dict:
    if i % 10 == 0:
        print()
    print(obj, end=', ')
    i += 1
print()
# Get the input and check for validity of the object of interest
while True:
    keyword = input("Name the object that you want to draw: ")
    keyword = keyword.split()
    instance = 0
    for word in keyword:
        if word in obj_dict:
            instance += 1
            keyword2 = word + ''
    if instance == 0:
        print("Your object has to be one of the given objects")
    elif instance != 1:
        print("Your search parament must include as most one object.")
    else:
        keyword = " ".join(keyword)
        break
# Get the input for size of the dataset
while True:
    try:
        number = int(input("Please input the dataset size: "))
        if number < 10:
            print("Your dataset size is too small! Increase it beyond 10.")
        else:
            break
    except:
        print('Your input must be an integer')
#
obj_dict[keyword2] = 'True'

try:
    search.search_image(keyword, keyword2, number)
    choice = 'delete'
# If the dataset for the keyword already existed, user input 'delete'
# to remove the existing dataset, download and conduct object detection
# on the new dataset. Otherwise, user input 'keep' to use the existing dataset.  
except:
    print("Dataset " + keyword2 + ' already existed')
    print('If you want to kept this dataset, please input "keep". '
          'Otherwise, input "delete" to remove this dataset')
    while True:
        choice = input("Please indicate your choice: ")
        if choice == 'keep':
            break
        elif choice == 'delete':
            os.rmdir(os.path.join(curdir, keyword2))
            search.search_image(keyword, keyword2, number)
            break
        else:
            print("You must answer 'keep' or 'delete'")            
if choice == 'delete':
    count = detection.detect_object(obj_dict, keyword2)
else:
    count = len(os.listdir(os.path.join(curdir, keyword2))) - 1  
# User inputs the filename of the image used to color 
while True:
    filename = input("Please input sample image file: ")
    try:
        image.get_channel(filename, 'red')
        break
    except:
        print("Invalid image, please try another file.")
# Identify the main colors of the dataset
red, green, blue, chances, processed_image = demo_draw.all_images_color(count, keyword2)
demo_draw.demo_draw(filename, red, green, blue, chances, processed_image)
