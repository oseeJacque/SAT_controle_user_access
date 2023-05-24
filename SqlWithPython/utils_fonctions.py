import os,re,string,random
from models import User 
from PIL import Image 
from pyzbar.pyzbar import decode
import qrcode 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Créez un moteur de base de données SQLite
engine = create_engine('sqlite:///mydatabase.db', echo=True)

# Créez une session pour interagir avec la base de données
Session = sessionmaker(bind=engine)
session = Session() 


#Générateur de chaine de 32 caractère
"""
    Cette fonction permet de générer un texte de 32 caractère 
    Paramètre: pas de paramètre 
    return :String (Texte de 32 caractère)
"""
def generate_random_string(length=32):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


#Generateur de code qr
""" 
Cette fonction est chargée de générer du code QR 
paramettre: 
    content="String" 
    security_code="String"
    
return:
    path_of_qr_image:String (chemin du stockage de l'image qr)
    content:String(le contenu du code qr)
    
"""
def generated_qr_code(security_code):
    
    #Récuperation de la liste des utilisateurs
    users=session.query(User).all()
    
    #Vérification si le contenur du ocde_qr existe déjà
    content_is_exist=True
    while content_is_exist:
        content=generate_random_string()
        for user in users: 
            if user.qr_code == content:
                content_is_exist=True 
                break
            else:
                content_is_exist=False         
    #Creation du code QR à partir de la donnée spécifier  
    qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=10,border=4)
    qr.add_data(content)
    qr.make(fit=True) 
    
    
    #Génération de l'image du code QR 
    image = qr.make_image(fill_color="black",back_color="white") 
    
    #Chemin de l'enregistrement de l'image 
    path_of_qr_image=f"qrcode_{security_code}.png"
    
    #Chemin complet pour de l'image
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    code_qr_dir = os.path.join(BASE_DIR, "codes_qr") 
    complete_path = os.path.join(code_qr_dir,f"qrcode_{security_code}.png")
    
    #Enregistremet de l'image 
    image.save(complete_path) 
    
    
    return path_of_qr_image,content



#Lecteur de Code QR
""" 
Cette fonction permet de decoder un code QR à partir de son image 
paramettre:
    image_path:String (chemin de l'image) 

return: 
    r_code_content:String (contenu du code QR)
"""
def read_qr_code(image_path):
    try:
        #Chemin complet pour de l'image
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        code_qr_dir = os.path.join(BASE_DIR, "codes_qr") 
        complete_path=os.path.join(code_qr_dir,f"{image_path}")
        
        #Ouverture de l'image QR
        image=Image.open(complete_path) 
        
        #Decoder l'image 
        qr_codes=decode(image) 
        
        if qr_codes:
            #recuperation du contenu du code qr
            qr_code_content=qr_codes[0].data.decode('utf-8')
            return qr_code_content
        else:
            print("Aucun code QR trouvé dans l'image")
            return None 
    except Exception as e:
        print(f"Une erreur s'est produite lors de la lecture du code QR : {str(e)}")  
        return None


#Définition de la fonction save_user pour l'enregistrement d'un utilisateur 
"""
Paramètre: 
data={
    "lastname":String, 
    "firstname":String, 
    "email":String,
    "code_security":String, 
    "qr_code":String, 
    "qr_image":String,
} 
return :
True if user save is succefull and False else
"""
def save_user(data):
    
    try:
         # Créez un nouvel utilisateur
        new_user = User(
            lastname=data["lastname"],
            firstname=data["firstname"],
            email=data["email"],
            code_security=data["code_security"],
            qr_code=data["qr_code"],
            qr_image=data["qr_image"]
        )

    # Ajoutez l'utilisateur à la session
        print ("yes ")
        session.add(new_user) 
    # Validez les modifications
        session.commit()
        
        return True
    except Exception as e:
         # Gérer l'erreur
        print(f"Une erreur s'est produite lors de l'ajout de l'utilisateur : {str(e)}") 
        return False
    finally:
        
        # Fermez la session
        session.close() 
        

#Rechercher un tuilisateur  
""" 
    Cette methode permet de recupérer les informations d'un utilisateur si ce dernier existe 
    Paramettre:
        by:String (Methode de recherhce utilisé)
        value:String (la clé de recherche)
        
    retourn:
        User:User (L'utilisateur recherhcer)
"""
def get_user(by, value):
    
    try:
        
        if by == 'qr': 
            #Recupérer tous les utilisateurs existant dans la base de donées
            users=session.query(User).all()
            
            #Parcouru la listes des utilisateurs pour voir le code qr de celui qui correspond a value 
            for user in users:
                print(user.qr_code)
                print(f"la valeur est {value}")
                if user.qr_code == value :
                    return user
            return None
        else:
            return None
    except Exception as e:
        print(f"Une erreur s'est produite lors de la lecture du code QR : {str(e)}")
        return None 
    

#Verification si un text est un mail 
def is_email(text):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, text):
        return True
    else:
        return False
