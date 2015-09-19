"""Running this file creates the database required for the Item Catalog web application"""

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime
 
Base = declarative_base()

# class User(Base):
#     __tablename__ = 'user'
#    
#     id = Column(Integer, primary_key=True)
#     name = Column(String(250), nullable=False)
#     email = Column(String(250), nullable=False)
#     picture = Column(String(250))


class Category(Base):
    __tablename__ = 'category'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), unique=True, nullable = False)
    # user_id = Column(Integer,ForeignKey('user.id'))
    # user = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
            'id'    : self.id,
            'name'  : self.name
       }

class Item(Base):
    __tablename__ = 'item'


    id = Column(Integer, primary_key = True)
    name =Column(String(80), unique=True, nullable = False)
    description = Column(String(250), nullable = False)
    image_url = Column(String(250))
    last_updated = Column(DateTime, onupdate=datetime.datetime.utcnow, default=datetime.datetime.utcnow, nullable = False)
    category_id = Column(Integer,ForeignKey('category.id'))
    category = relationship(Category)
    # user_id = Column(Integer,ForeignKey('user.id'))
    # user = relationship(User)


    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
            'id'            : self.id,
            'name'          : self.name,
            'description'   : self.description,
            'image'         : self.image_url
       }



engine = create_engine('sqlite:///catalog.db')
 

Base.metadata.create_all(engine)
