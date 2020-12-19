# The Clockwork Artist
A very basic AI project by Vuong Kha Sieu and Dinh Gia Han
# Introduction
This program tries to color an image containing the object of interest after learning its color pattern from the images on the Internet. 
There are 4 modules including:

**search.py**, This module uses Google Image Search library to download images containing the object of interest on the Internet.

**detection.py**, This module uses the pre-trained model RetinaNet to detect the object and return its images extracted from the original dataset.

**demo_draw.py**, This module learns the color of the object by identifying the main colors in the dataset and demo the coloring step on a given sample image.

**main.py**, This module asks for the user’s input for the object’s name, the size of the dataset, the image used for coloring. It then goes on downloading and learning the dataset to generate a colored image.

## Limitations
- Detectable objects are predefined by Detection Classes – ImageAi; thus, the number of detectable objects using this program is limited. See the available options in the main function of this program or [this link](https://imageai.readthedocs.io/en/latest/detection/index.html).

- The demo_draw module requires the image used for demo coloring to have the object shown in pixels whose RGB < 242 and the background should be in white (RGB=255)

# Prerequisites
Before executing any code in this repo, you must have the following dependencies installed:
-   Python 3.6
-   opencv-python==4.4.0.46
-   tensorflow==1.5
-   windows-curses==2.2.0
-   keras==2.1.5
-   h5py==2.10.0
-   imageai==2.1.5
-   Google-Images-Search==1.3.4
-   csc121

Note on numpy: If you get numpy related errors, please install numpy == 1.19.3

Note on google_image_download: If you have any problem downloading a large amount of image, please replace 
"fetch_resize_cache.py" module inside your Google_Images_Search library with the one in this repo.

Also you have to download the AI models here and place them in a folder named "models" in the root directory of this repo:
-   https://github.com/OlafenwaMoses/ImageAI/releases/tag/1.0/
# Usage
Please run "main.py" to execute the program
# Old codes
Old codes can be found inside "old_codes" folder. Codes are stored by date modified.