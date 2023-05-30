import os,face_recognition
from Faces.verify_face import verify_face
from typing import Tuple
from face_detection import convert_image_to_numpy_array
from verify_face import verify_face
import cv2


def search_face(image)->Tuple[str,float,None]:
    """Searches for a person in the collection of faces using the given image.

    Args:
        image (numpy.array): Image to search.

    Returns:
        tuple: A tuple containing the name, probability, and image with the framed face if a person is found.
               If no person is found, returns (None, 0, None).
    """ 
    #Get user_images folder
    BASE_DIR=os.path.dirname(os.path.abspath(__file__))
    user_imgaes_dir=os.path.join(BASE_DIR,"user_images") 
    
# Initialize variables to store the best search
    #The user name
    best_search_name = None
    
    # Probality for image to be it
    best_search_probability = 0  
    
    #Image  search with framed 
    best_search_image = None   #Image 
  
  #Iteral the user_imgaes_dir folder to determine the users folders
    for image_dir_name in os.listdir(user_imgaes_dir):
        
        image_dir_path=os.path.join(user_imgaes_dir,image_dir_name)
        #Iterate each person image dir
        for user_image_dir in os.listdir(image_dir_path): 
            facepath = os.path.join(image_dir_path,user_image_dir)
            
            #load image with face_recognition
            known_image=face_recognition.load_image_file(facepath) 
            
            #Verify the image and get it probability
            probability = verify_face(image_dir_name,known_image) 
            
            if probability > best_search_probability:
                best_search_probability = probability 
                best_search_name = image_dir_name
                best_search_image = known_image  
    if best_search_name is not None:       
        return best_search_name,best_search_probability,best_search_image
    
    return None, 0, None

  

search_face(convert_image_to_numpy_array("./person/emilia-clarke/1.jpg"))