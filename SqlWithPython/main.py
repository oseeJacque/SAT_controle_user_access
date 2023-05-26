from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils_fonctions import is_email

from models import User
from utils_fonctions import generated_qr_code, get_user, read_qr_code, save_user

# Create an SQLite database engine
engine = create_engine('sqlite:///mydatabase.db', echo=True)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session() 

#Get all user from dataBase 
users=session.query(User).all()
#Variable to check if the text entered for the email is an email
isMail=True

#Register users with the keyboard
print("USER REGISTRATION ") 

#LastName 
print("Lastname: ")
nom=input()

#Firstname
print("\nFirstname: ")
prenom=input()

#Email 
while isMail: 
    print("\nEmail:")
    email=input() 
    if is_email(email):
        isMail=False
    else:
        isMail=True

#Security code 
print("\nSecurity Code:")
code_security=input()

    
#Code QR 
qr_image,code_qr=generated_qr_code(code_security)

# Create a user
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
    print("User registration is success")
else:
    print("User registration is fail")


"""
#User vérification on the database
for user in users:
    get_user('qr',value=read_qr_code(user.qr_image))
"""
