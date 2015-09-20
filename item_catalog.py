"""item_catalog.py generates a Python Flask website for Udacity's Full Stack Web Developer Nanodegree Project 3"""

import os
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, session

from flask_wtf.csrf import CsrfProtect
# from wtf_form_functions import MyForm
from wtf_form_functions import createItemForm

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker, exc
from catalog_database_setup import Base, Category, Item


engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

db_session = DBSession()

app = Flask(__name__)



### testing flask_wtf
@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = RegistrationForm()
    if request.method=='POST' and form.validate:
            return redirect('/success')
    return render_template('submit.html', form=form)

@app.route('/success', methods=('GET', 'POST'))
def success():
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        # user = User(form.username.data, form.email.data,
        #             form.password.data)
        # db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('showCatalog'))
    return render_template('register.html', form=form)
### testing flask_wtf



#Fake categories
categories = [{'name': 'Soccer', 'id': '1'}, {'name': 'Basketball', 'id': '2'}, {'name': 'Baseball', 'id': '3'}, {'name': 'Frisbee', 'id': '4'}, {'name': 'Snowboarding', 'id': '5'}, {'name': 'Rock Climbing', 'id': '6'}, {'name': 'Foosball', 'id': '7'}, {'name': 'Skating', 'id': '8'}, {'name': 'Hockey', 'id': '9'}]
category = {'name': 'Snowboarding', 'id': '5'}

# items = [{'id': '1', 'name': 'Stick', 'description': 'Used to hit the puck.', 'image_url': 'http://example.com/stick.png', 'last_updated': '2015-09-19 10:28:00', 'category_id': '9'}, {'id': '2', 'name': 'Goggles', 'description': 'Used to protect your eyes.', 'image_url': 'http://example.com/goggles.png', 'last_updated': '2015-09-20 09:27:00', 'category_id': '5'}, {'id': '3', 'name': 'Snowboard', 'description': 'Used to travel down the mountain.', 'image_url': 'http://example.com/snowboard.png', 'last_updated': '2015-09-18 10:27:00', 'category_id': '5'}, {'id': '3', 'name': 'Shinguards', 'description': 'Keeps shins safe from kicks.', 'image_url': 'http://example.com/shinguard.png', 'last_updated': '2015-09-16 07:14:00', 'category_id': '1'}]
items = [{'id': '2', 'name': 'Goggles', 'description': 'Used to protect your eyes.', 'image_url': 'http://example.com/goggles.png', 'last_updated': '2015-09-20 09:27:00', 'category_id': '5'}, {'id': '3', 'name': 'Snowboard', 'description': 'Used to travel down the mountain.', 'image_url': 'http://example.com/snowboard.png', 'last_updated': '2015-09-18 10:27:00', 'category_id': '5'}]
item = {'id': '2', 'name': 'Goggles', 'description': 'Used to protect your eyes.', 'image_url': 'http://example.com/goggles.png', 'last_updated': '2015-09-20 09:27:00', 'category_id': '5'}


"""This route is the root of the web application and returns the catalog categories and top ten recent items."""
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = db_session.query(Category).order_by(asc(Category.name))
    last_items = db_session.query(Item, Category).filter(Item.category_id==Category.id).order_by(desc(Item.last_updated)).limit(10)
    return render_template('showCatalog.html', categories=categories, last_items=last_items )

"""This route shows all items for a particular category."""
@app.route('/catalog/<string:category_name>/items/')
def showCategory(category_name):
    return render_template('showCategory.html', category=category, items=items, item_count=str(len(items)) )

"""This route allows a user to create a new item for a given category."""
@app.route('/catalog/<string:category_name>/new/')
def createItem(category_name, methods=('GET', 'POST')):
    # if item_name.lower() == 'items':
    #     return "Items is a reserved word for this application. You cannot use it as the name of an item."
    categories = db_session.query(Category).order_by(asc(Category.name))
    form = createItemForm(request.form)
    form.category.choices =  [(c.id, c.name) for c in categories]
    
    if request.method == 'POST' and form.validate():
        # user = User(form.username.data, form.email.data,
        #             form.password.data)
        # db_session.add(user)
        flash('Your new item has been entered')
        return redirect(url_for('showCategory'))
    return render_template('createItem.html', form=form)
    #return "This page will allow the user to create a new item for the category: %s" % category_name

"""This route allows a user to edit a specific item they created."""
@app.route('/catalog/<string:item_name>/edit/')
def editItem(item_name):
    return "This page will allow the user to edit the item: '%s'" % item_name

"""This route allows a user to delete a specific item they created."""
@app.route('/catalog/<string:item_name>/delete/')
def deleteItem(item_name):
    return "This page will allow the user to delete the item: %s" % item_name

"""This route shows details about a single item."""
@app.route('/catalog/<string:category_name>/<string:item_name>/')
def showItem(category_name, item_name):
    return render_template('showItem.html', item=item)

"""This route handles logging in the user using the Google OAuth API."""
@app.route('/catalog/login/')
def login():
    return "This page will process the oAuth login."

"""This route handles logging out the user using the Google OAuth API."""
@app.route('/catalog/logout/')
def logout():
    return "This page will process the oAuth logoff."

# implement Cross Site Request Forgery protection from flask_wtf
csrf = CsrfProtect()

if __name__ == '__main__':
    app.secret_key = '\r\x94b\xf3\xa5\xa5\x15\x13o\xa0DB\xa0m\x0e\xf1i\xa4"\xfeEW&W\xba\xc9Ko\x93'
    csrf.init_app(app)
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
