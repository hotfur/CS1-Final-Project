"""
Search and download object images
Author: Vuong Kha Sieu & Dinh Gia Han
Date: 18/12/2020
"""
from google_images_search import GoogleImagesSearch
import os

# you can provide API key and CX using arguments,
# or you can set environment variables: GCS_DEVELOPER_KEY, GCS_CX


def search_image(keyword, keyword2, number):
    """
    Download images that contain a specific object.

    Parameters:
        - keyword: user's input for the object of interest 
        - keyword2: the word in user's input that is detectable by imageAI
        - number: an integer shows the desired number of images to download
    Returns: None
    """
    # Provide API key and project CX
    gis = GoogleImagesSearch('AIzaSyBQFJU9zOpofCk2V8-b7bmtQEYP5raGZec', '6922f47f7f04d0785')
    current_dir = os.getcwd()
    
    # Define search paramemts
    _search_params = {
        'q': keyword,
        'num': number,
    }
    # Create a directory named with keyword2 in the current working directory
    # Download the images with the search params defined
    # For each image downloaded, save it in the keyword2-directory
    os.mkdir(os.path.join(current_dir, keyword2))
    gis.search(search_params=_search_params)
    for image in gis.results():
        try:
            image.download(os.path.join(current_dir, keyword2))
        except OSError:
            continue
