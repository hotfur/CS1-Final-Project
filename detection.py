"""
This module separates an object of interest from a image
Author: Vuong Kha Sieu & Dinh Gia Han
Date: 18/12/2020
"""
from imageai.Detection import ObjectDetection
import os

def detect_object(obj_dict, keyword):
    """
    Using pre-trained model RetinaNet to detect the object in the images
    downloaded, return the images of the object extracted from the original
    images.

    Parameters:
        - obj_dict: a list of objects that ObjectDetection class can detect.
                    Only the object equals keyword inputted by the user is
                    set as 'True' for detection
        - keyword: a string of the object of interest
    Returns:
        - count: the number of directories containing the images of the object
                 extracted from the original images
    """
    detector = ObjectDetection()
    model_path = "./models/resnet50_coco_best_v2.0.1.h5"
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(model_path)
    detector.loadModel()

    execution_path = os.path.join(os.getcwd(), keyword)
    # For summing up the number of such directories
    count = 0
    # Creat a list of all directories in the current working directories
    image_list = os.listdir(path=execution_path)
    for image in image_list:
        try:
            detections, objects_path = detector.detectCustomObjectsFromImage(custom_objects=obj_dict, input_image=os.path.join(execution_path , image),
                                                                             output_image_path=os.path.join(execution_path , 'new'+image), minimum_percentage_probability=50,
                                                                             extract_detected_objects=True)
        except:
            # If errors, removes current image
            os.remove(os.path.join(execution_path , image))
            try:
                # Try to savage processed objects within corrupted image
                os.rename(os.path.join(execution_path, 'new' + image + '-objects'),
                          os.path.join(execution_path, str(count)))
                count += 1
                continue
            except:
                continue
        # Remove the original images, the images with markings left after the detection process  
        os.remove(os.path.join(execution_path, image))
        os.remove(os.path.join(execution_path, 'new' + image))
        # Rename the directories containing the extracted images with numbers.
        
        try:
            os.rename(os.path.join(execution_path , 'new' + image + '-objects'), os.path.join(execution_path , str(count)))
            count += 1
        except FileNotFoundError:
            continue
    return(count)
