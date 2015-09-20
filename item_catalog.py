"""item_catalog.py generates a Python Flask website for Udacity's Full Stack Web Developer Nanodegree Project 3"""

import os
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, session

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker, exc
from catalog_database_setup import Base, Category, Item


engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

db_session = DBSession()

app = Flask(__name__)

"""This route is the root of the web application and returns the catalog categories and top ten recent items."""
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = db_session.query(Category).order_by(asc(Category.name))
    last_items = db_session.query(Item, Category).filter(Item.category_id==Category.id).order_by(desc(Item.last_updated)).limit(10)
    return render_template('catalog.html', categories=categories, last_items=last_items )

"""This route shows all items for a particular category."""
@app.route('/catalog/<string:category_name>/items/')
def showItems(category_name):
    return "This page will show all items for the category: %s." % category_name

"""This route shows details about a single item."""
@app.route('/catalog/<string:category_name>/<string:item_name>/')
def showItem(category_name, item_name):
    return "This page will show details about the item %s for category: %s." % (item_name, category_name)

"""This route allows a user to create a new item for a given category."""
@app.route('/catalog/<string:category_name>/new/')
def createItem(category_name):
    # if item_name.lower() == 'items':
    #     return "Items is a reserved word for this application. You cannot use it as the name of an item."
    return "This page will allow the user to create a new item for the category: %s" % category_name

"""This route allows a user to edit a specific item they created."""
@app.route('/catalog/<string:item_name>/edit/')
def editItem(item_name):
    return "This page will allow the user to edit the item: '%s'" % item_name

"""This route allows a user to delete a specific item they created."""
@app.route('/catalog/<string:item_name>/delete/')
def deleteItem(item_name):
    return "This page will allow the user to delete the item: %s" % item_name

"""This route handles logging in the user using the Google OAuth API."""
@app.route('/catalog/login/')
def login():
    return "This page will process the oAuth login."

"""This route handles logging out the user using the Google OAuth API."""
@app.route('/catalog/logout/')
def logout():
    return "This page will process the oAuth logoff."
    
if __name__ == '__main__':
    app.secret_key = '\r\x94b\xf3\xa5\xa5\x15\x13o\xa0DB\xa0m\x0e\xf1i\xa4"\xfeEW&W\xba\xc9Ko\x93'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
