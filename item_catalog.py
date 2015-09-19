"""item_catalog.py generates a Python Flask website for Udacity's Full Stack Web Developer Nanodegree Project 3"""

import os
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash


app = Flask(__name__)

"""This route is the root of the web application and returns the catalog categories and top ten recent items."""
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    return "This page will show all categories and the top ten latest items."

"""This route shows all items for a particular category."""
@app.route('/catalog/<string:category_name>/items/')
def showItems(category_name):
    return "This page will show all items for a specific category name."

"""This route shows details about a single item."""
@app.route('/catalog/<string:category_name>/<string:item_name>/')
def showItem(category_name, item_name):
    return "This page will show details about a single item."

"""This route allows a user to create a new item for a given category."""
@app.route('/catalog/<string:category_name>/new/')
def createItem(category_name):
    return "This page will allow the user to create a new item for a given category."

"""This route allows a user to edit a specific item they created."""
@app.route('/catalog/<string:item_name>/edit')
def editItem(item_name):
    return "This page will allow the user to edit a specific item."

"""This route allows a user to delete a specific item they created."""
@app.route('/catalog/<string:item_name>/delete')
def deleteItem(item_name):
    return "This page will allow the user to delete a specific item they created."

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