import cv2
import numpy as np
from PIL import Image
from deepface import DeepFace



#Detect face from image function
def detect_face(image):
    """Detects a face in an image and flips the image with the framed face.

    Args:
        image (numpy.array): Enter Image

    Returns:
        numpy.array: Image with the framed face
    """
    face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
    faces=face_cascade.detectMultiScale(image,scaleFactor=1.1,minNeighbors=5,minSize=(30,30)) 
    
    if len(faces) == 0 :
        print("No face detect") 
        return None 
    elif len(faces) > 1:
        print ("We are detecting more than two face")
        
    else: 
        (x, y, w, h) = faces [0]
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2) 
        return image  
  
    
#Emotion detector 
def get_emotion(image):
    """This function allow to get emotion from image

    Args:
        image (numpy.array): Image whixch will be analyze

    Returns:
        _type_: _description_
    """
    detected_face = detect_face(image)

    if detected_face is None:
        return None

    face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2RGB)
    emotions = DeepFace.analyze(face, actions=['emotion'])

    return emotions[0]


 
#Convert image to Numpy _array
def convert_image_to_numpy_array(image_path):
    """This function allow to convert image to numpy table

    Args:
        image_path (String):The path of the image

    Returns:
        numpy.array: numpy.array from image
    """
    pil_image = Image.open(image_path).convert("L") 
    size = (550, 550)
    final_image = pil_image.resize(size, Image.Resampling.LANCZOS)
    image_array = np.array(final_image, "uint8")
    return image_array 
    
    
print(get_emotion(convert_image_to_numpy_array("./person/personhappy.jpg")))
