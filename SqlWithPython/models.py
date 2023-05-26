from sqlalchemy import create_engine,Column,Integer,String 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base 

#Create an SQLite database engine
engine=create_engine('sqlite:///mydatabase.db',echo=True) 

#Creates a base class for ORM classes 

Base=declarative_base()

#Define User class 
class User(Base): 
    __tablename__='users'
    id=Column(Integer,primary_key=True)
    lastname=Column(String)
    firstname=Column(String) 
    email=Column(String,unique=True)
    code_security = Column(String)
    qr_code = Column(String)
    qr_image=Column(String,unique=True)
    
    def login(self):
        # login logic
        pass

    def register(self):
        # Registration logic
        pass

    def forgot_password(self):
        # Registration logic
        pass

    def logout(self):
        # Logout Logic
        pass

#Creates database and the tables
Base.metadata.create_all(engine)