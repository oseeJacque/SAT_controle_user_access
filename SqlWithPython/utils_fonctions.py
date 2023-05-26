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
def generate_random_string(length=32):
    """
    Cette fonction permet de générer un texte de 32 caractère 
    Paramètre: pas de paramètre 
    return :String (Texte de 32 caractère)
    """
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


#Generateur de code qr
def generated_qr_code(security_code):
    """ 
    Cette fonction est chargée de générer du code QR 
    paramettre: 
        content="String" 
        security_code="String"
        
    return:
        path_of_qr_image:String (chemin du stockage de l'image qr)
        content:String(le contenu du code qr)
    """
    #Récuperation de la liste des utilisateurs
    users=session.query(User).all()
    
    #Vérification si le contenur du ocde_qr existe déjà
    content_is_exist=True
    while content_is_exist:
        content=generate_random_string()
        
        #Vérifier s'il y a plusieurs utilisateur dans la base de donnée
        if len(users) > 0:
            #Vérification de l'unicité du text généré
            for user in users: 
                if user.qr_code == content:
                    content_is_exist=True 
                    #print("hi")
                    break
                else:
                    content_is_exist=False 
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
    
    #Enregistrement de l'image 
    image.save(complete_path) 
    
    
    return path_of_qr_image,content



#Lecteur de Code QR
def read_qr_code(image_path):
    """ 
    Cette fonction permet de decoder un code QR à partir de son image 
    paramettre:
        image_path:String (chemin de l'image) 

    return: 
        r_code_content:String (contenu du code QR)
    """
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
def save_user(data):
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
def get_user(by, value,is_user_find=False):
    """ 
    Cette methode permet de recupérer les informations d'un utilisateur si ce dernier existe 
    Paramettre:
        by:String (Methode de recherhce utilisé)
        value:String (la clé de recherche)
        
    retourne:
        User:User (L'utilisateur recherhcer)
    """
    try:  
        if by == 'qr': 
            #Recupérer tous les utilisateurs existant dans la base de donées
            users=session.query(User).all()
            
                #Parcouru la listes des utilisateurs pour voir le code qr de celui qui correspond a value 
            for user in users:
                if user.qr_code == value :
                    is_user_find=True
                    #Demander le code de sécurité à l'utilisateur
                    print("Veuillez saisir votre code de sécurité ")
                    code_security=input()
                    if code_security == user.code_security: 
                        print(
                            f"\n Nom: {user.lastname}\nPrénom: {user.firstname}\n Email: {user.email}\n Code de Sécurité: {user.code_security}\n Contenu du Code QR: {user.qr_code}\n QR Image source: {user.qr_image}"
                        )
                    else:
                        print("Le code de sécurité entré est invalide")
                       # return user
                #return None
        else:
            print("Aucun utilisateur trouvé dans la base de donnée")
            #return None
    except Exception as e:
        print(f"Une erreur s'est produite lors de la lecture du code QR : {str(e)}")
        return None 
  

#Verification si un text est un mail 
def is_email(text):
    """Cette fonction permet de verifiér si un test est un email

    Args:
        text (String): Le text à vérifier

    Returns:
       bool: True si le texte est un email et False dans le cas contraire 
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, text):
        return True
    else:
        return False
