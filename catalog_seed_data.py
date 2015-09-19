"""Running this file seeds the database with the base categories."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from catalog_database_setup import Base, Category, Item

engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()

#Add Base Categories
for name in ["Soccer", "Basketball", "Baseball", "Frisbee", "Snowboarding", "Rock Climbing", "Foosball", "Skating", "Hockey"]:
    newCategory = Category(name = name )
    session.add(newCategory)
session.commit()

