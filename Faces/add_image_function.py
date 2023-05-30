import os
from face_detection import convert_image_to_numpy_array
import cv2

def add_face(name,image):
    """Adds a new face image to the person with the given name.

    Args:
        name (str): Name of the person.
        image (numpy.array): Face image to add.

    Returns:
        bool: True if the face image is successfully added, False otherwise.
    """ 
    
    #Get the directory for the name 
    BASE_DIR=os.path.dirname(os.path.abspath(__file__)) 
    directory=os.path.join(os.path.join(BASE_DIR,"user_images"),name) 
    
    #Generate a unique filename for the new image face 
    filename=f'profile_{len(os.listdir(directory))+1}.jpg'
    filepath=os.path.join(directory,filename)
    
    #Let's save the new image 
    try: 
        cv2.imwrite(filepath,image)
        print("New face image added successfully.")
        return True
    except Exception as e:
        print("Error adding new face image:", str(e))
        return False

print(add_face("emilia-clarke",convert_image_to_numpy_array("./person/emilia-clarke/2.jpg")))
print(add_face("kit-harington",convert_image_to_numpy_array("./person/kit-harington/2.jpg")))
print(add_face("nikolaj-coster-waldau",convert_image_to_numpy_array("./person/nikolaj-coster-waldau/2.jpg")))
print(add_face("jacques",convert_image_to_numpy_array("./person/jacques/2.jpg")))


