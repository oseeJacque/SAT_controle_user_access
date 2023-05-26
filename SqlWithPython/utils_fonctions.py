import os,re,string,random
from models import User 
from PIL import Image 
from pyzbar.pyzbar import decode
import qrcode 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create an SQLite database engine
engine = create_engine('sqlite:///mydatabase.db', echo=True)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session() 


#32 character string generator
def generate_random_string(length=32):
   
    """This function generates a text of 32 characters

    Returns:
        String: 32 character random text
    """
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


#Code qr générator
def generated_qr_code(security_code):
    """This function is responsible for generating QR code

    Args:
        security_code (String): Security code of User

    Returns:
        String: Paths of code qr image
        String: Code qr content

    """
    #User list retrieval
    users=session.query(User).all()
    
    #Checking if the content of ocde_qr already exists
    content_is_exist=True
    while content_is_exist:
        content=generate_random_string()
        
        #Vérifier s'il y a plusieurs utilisateur dans la base de donnée
        if len(users) > 0:
            #Verification of the uniqueness of the generated text
            for user in users: 
                if user.qr_code == content:
                    content_is_exist=True 
                    break
                else:
                    content_is_exist=False 
        else:
              content_is_exist=False 
  
    #Creation of the QR code from the specified data  
    qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=10,border=4)
    qr.add_data(content)
    qr.make(fit=True) 
    
    #Generating the QR code image
    image = qr.make_image(fill_color="black",back_color="white") 
    
    #Image save path
    path_of_qr_image=f"qrcode_{security_code}.png"
    
    #Full path for image storage
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    code_qr_dir = os.path.join(BASE_DIR, "codes_qr") 
    complete_path = os.path.join(code_qr_dir,f"qrcode_{security_code}.png")
    
    #Saving image 
    image.save(complete_path) 
    
    
    return path_of_qr_image,content



#QR Code Reader
def read_qr_code(image_path):
    """This function allows you to decode a QR code from its image

    Args:
        image_path (String): Code QR image path

    Returns:
        String: QR code content from image.If the image is empty we return None
    """
    try:
        #Full path for image
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        code_qr_dir = os.path.join(BASE_DIR, "codes_qr") 
        complete_path=os.path.join(code_qr_dir,f"{image_path}")
        
        #Opening the QR image
        image=Image.open(complete_path) 
        
        #Decoding the image
        qr_codes=decode(image) 
        
        if qr_codes:
            #qr code content recovery
            qr_code_content=qr_codes[0].data.decode('utf-8')
            return qr_code_content
        else:
            print("No QR code found in image")
            return None 
    except Exception as e:
        print(f"An error occurred while reading the QR code: {str(e)}")  
        return None


#Defining the save_user function for saving a user QR code
def save_user(data):
    """_summary_

    Args:
        data (Dictionary): data={
        "lastname":String, 
        "firstname":String, 
        "email":String,
        "code_security":String, 
        "qr_code":String, 
        "qr_image":String,
    }

    Returns:
        Bool: True if user save is succefull and False else
    """
    try:
         # Create new User
        new_user = User(
            lastname=data["lastname"],
            firstname=data["firstname"],
            email=data["email"],
            code_security=data["code_security"],
            qr_code=data["qr_code"],
            qr_image=data["qr_image"]
        )

    # Add the new User to session
        print ("yes ")
        session.add(new_user) 
    # Validate the new modification from database
        session.commit()
        
        return True
    except Exception as e:
        print(f"An error occurred while adding the user: {str(e)}") 
        return False
    finally:
        
        # Fermez la session
        session.close() 
        

#Search user in the data base  
def get_user(by, value,is_user_find=False):
    """This method makes it possible to retrieve the information of a user if the latter exists

    Args:
        by (String): Identification Method
        value (String): User code QR content
        is_user_find (bool, optional): True if user is in data base.

    Returns:
        User: Return User if it's find otherwise return None
    """
    try:  
        if by == 'qr': 
            #Retrieve all users from Data base
            users=session.query(User).all()
            
                #Browse the list of users to see the qr code of the one that corresponds to value
            for user in users:
                if user.qr_code == value :
                    is_user_find=True
                    #Ask user for security code
                    print("Please enter your security code ")
                    code_security=input()
                    if code_security == user.code_security: 
                        print(
                            f"\n Lastname: {user.lastname}\nFirstname: {user.firstname}\n Email: {user.email}\n Security Code: {user.code_security}\n Code QR content: {user.qr_code}\n QR Image source: {user.qr_image}"
                        )
                    else:
                        print("The security code entered is invalid")
                       # return user
                #return None
        else:
            print("No user found in database")
            #return None
    except Exception as e:
        print(f"An error occurred while reading the QR code: {str(e)}")
        return None 
  
#Checking if a text is an email 
def is_email(text):
    """This function allows you to check if a test is an email

    Args:
        text (String): Text to check

    Returns:
        Bool: True if text is email and False If not 
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, text):
        return True
    else:
        return False
