from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils_fonctions import is_email

from models import User
from utils_fonctions import generated_qr_code, get_user, read_qr_code, save_user

# Créez un moteur de base de données SQLite
engine = create_engine('sqlite:///mydatabase.db', echo=True)

# Créez une session pour interagir avec la base de données
Session = sessionmaker(bind=engine)
session = Session() 

#Get all user from dataBase 
users=session.query(User).all()
is_qr_exist=True
isMail=True

#Enregistrer les utilisateurs avec le clavier 
print("ENREGISTREMENT D'UN UTILISATEUR ") 

#prenoms 
print("Nom: ")
nom=input().split(' ')

#Nom
print("\nPrénoms: ")
prenom=input().split(' ')

#email 
while isMail: 
    print("\nemail:")
    email=input() 
    if is_email(email):
        isMail=False
    else:
        isMail=True

#Code de sécurité 
print("\nCode de Sécurité:")
code_security=input()

    
#Code QR 
qr_image,code_qr=generated_qr_code(code_security)

# Créez un nouvel utilisateur
result=save_user(
    data={
    "lastname":nom, 
    "firstname":prenom, 
    "email":email,
    "code_security":code_security, 
    "qr_code":code_qr, 
    "qr_image":qr_image,
    }
)

if result:
    print("Utilisateur enregistré avec succès!!")
else:
    print("Enregistrement de l'utilisateur a echoué")

#Vérification de l'existance des utilisateur 
for user in users:
    print (get_user('qr',value=read_qr_code(user.qr_image)))

