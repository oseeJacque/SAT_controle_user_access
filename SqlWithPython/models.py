from sqlalchemy import create_engine,Column,Integer,String 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base 

#Creer un moteur de base de données SQLite 
engine=create_engine('sqlite:///mydatabase.db',echo=True) 


#Crée une classe de base pour les classes ORM  

Base=declarative_base()

#Définit la classe User  
class User(Base): 
    __tablename__='users'
    id=Column(Integer,primary_key=True)
    lastname=Column(String)
    firstname=Column(String) 
    email=Column(String,unique=True)
    code_security = Column(String)
    qr_code = Column(String), 
    qr_image=Column(String,unique=True)
    
    def login(self):
        # Logique de connexion
        pass

    def register(self):
        # Logique d'inscription
        pass

    def forgot_password(self):
        # Logique de récupération de mot de passe
        pass

    def logout(self):
        # Logique de déconnexion
        pass

#Créer la base de donnée et les tables 

Base.metadata.create_all(engine)