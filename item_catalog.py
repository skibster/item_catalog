#!/usr/bin/python
# -*- coding: utf-8 -*-

"""item_catalog.py generates a Python Flask website for Udacity's Full Stack Web Developer Nanodegree Project 3"""

import os
import json, dicttoxml
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, session, Response

from flask_wtf.csrf import CsrfProtect
from wt_form_functions import createItemForm, editItemForm
from werkzeug import secure_filename

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker, exc
from catalog_database_setup import Base, Category, Item, User

from flask import session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response
import requests

engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

db_session = DBSession()

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"

MISSING_IMAGE = 'static/missing_image.png'

"""This route is the root of the web application and returns the catalog categories and top ten recent items."""
@app.route('/')
@app.route('/catalog')
def showCatalog():
    categories = db_session.query(Category).order_by(asc(Category.name))
    last_items = db_session.query(Item, Category).filter(Item.category_id==Category.id).order_by(desc(Item.last_updated)).limit(10)
    return render_template('showCatalog.html', categories=categories, last_items=last_items )

"""This route is the root of the web application and returns each catalog category with all of its items in JSON."""
@app.route('/catalog/json')
def jsonCatalog():
    js = MakeDictionary()
    return jsonify(Category=js)

"""This route is the root of the web application and returns each catalog category with all of its items in XML."""
@app.route('/catalog/xml')
def xmlCatalog():
    xml = MakeDictionary()
    return Response(dicttoxml.dicttoxml(xml),  mimetype='application/xml')

"""This route shows all items for a particular category."""
@app.route('/catalog/<string:category_name>/items')
def showCategory(category_name):
    categories = db_session.query(Category).order_by(asc(Category.name))
    category = db_session.query(Category).filter_by(name=category_name).one()
    items = db_session.query(Item, Category).filter(Item.category_id==Category.id).filter_by(category_id=category.id)

    return render_template('showCategory.html', categories = categories, category_name=category_name, items=items, item_count=items.count() )

"""This route allows a user to create a new item for a given category."""
@app.route('/catalog/<string:category_name>/new', methods=('GET', 'POST'))
def createItem(category_name):
    # if item_name.lower() == 'items':
    #     return "Items is a reserved word for this application. You cannot use it as the name of an item."
    categories = db_session.query(Category).order_by(asc(Category.name))
    category = db_session.query(Category).filter_by(name=category_name).one()
    form = createItemForm(category=category.id)
    form.category.choices =  [(c.id, c.name) for c in categories]

    if request.method == 'POST' and form.validate_on_submit():
        newItem = Item( name=request.form['name'],
                        description = request.form['description'],
                        category_id = request.form['category'])
        db_session.add(newItem)
        db_session.commit()

        # now add image_url storing the file under the item's ID
        image_url= MISSING_IMAGE
        filename = secure_filename(form.photo.data.filename)
        if filename:
            image_dir = 'static/uploads/%s/' % newItem.id
            os.mkdir(image_dir)
            form.photo.data.save(image_dir + filename)
            image_url =  image_dir + filename

        newItem.image_url = image_url
        db_session.add(newItem)
        db_session.commit()

        category = db_session.query(Category).filter_by(id=request.form['category']).one()
        flash(u"“%s” has been successfully created." % newItem.name)
        return redirect(url_for('showCategory', category_name=category.name))
    return render_template('createItem.html', form=form, category_name=category_name)

"""This route allows a user to edit a specific item they created."""
@app.route('/catalog/<string:item_name>/edit', methods=['GET', 'POST'])
def editItem(item_name):
    categories = db_session.query(Category).order_by(asc(Category.name))    
    #item = db_session.query(Item, Category).filter(Item.category_id==Category.id).filter_by(name=item_name).one()
    item = db_session.query(Item).filter_by(name=item_name).one()
    category = db_session.query(Category).filter_by(id=item.category_id).one()
    form = editItemForm(name=item.name,
                        description=item.description,
                        category=item.category_id)
    form.category.choices =  [(c.id, c.name) for c in categories]
    
    if request.method == 'POST' and form.validate_on_submit():
        image_url=item.image_url
        filename = secure_filename(form.photo.data.filename)
        if filename:
            old_image = item.image_url
            if old_image != MISSING_IMAGE:
                os.remove(old_image)
            image_dir = 'static/uploads/%s/' % item.id
            if old_image == MISSING_IMAGE:
                os.mkdir(image_dir)
            form.photo.data.save(image_dir + filename)
            image_url =  image_dir + filename
        
        item = db_session.query(Item).filter_by(name=item_name).one()
        item.name = request.form['name']
        item.description = request.form['description']
        item.image_url = image_url
        item.category_id = request.form['category']
        db_session.add(item)
        db_session.commit()
        category = db_session.query(Category).filter_by(id=request.form['category']).one()
        flash(u"“%s” has been successfully edited." % item.name)
        return redirect(url_for('showCategory', category_name=category.name))
    return render_template('editItem.html', form=form, item=item, item_name=item_name, category_name=category.name)

"""This route allows a user to delete a specific item they created."""
@app.route('/catalog/<string:item_name>/delete', methods=['GET', 'POST'])
def deleteItem(item_name):
    item = db_session.query(Item).filter_by(name=item_name).one()
    category = db_session.query(Category).filter_by(id=item.category_id).one()

    if request.method == 'POST':
        old_image = item.image_url
        if old_image != MISSING_IMAGE:
            os.remove(old_image)
            old_dir = 'static/uploads/%s/' % item.id
            os.removedirs(old_dir)
        db_session.delete(item)
        db_session.commit()
        flash(u"“%s” has been succesfully deleted." % item.name)
        return redirect(url_for('showCategory', category_name=category.name))
    return render_template('deleteItem.html', item_name=(u"“%s”" % item_name), item=item, category_name=category.name)

"""This route shows details about a single item."""
@app.route('/catalog/<string:category_name>/<string:item_name>', methods=['GET'])
def showItem(category_name, item_name):
    item = db_session.query(Item).filter_by(name=item_name).one()
    return render_template('showItem.html', item=item, category_name=category_name)

"""This route handles logging in the user using the Google OAuth API."""
@app.route('/catalog/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    session['state'] = state
    return render_template('login.html', STATE=state)

"""This route handles logging out the user using the Google OAuth API."""
@app.route('/catalog/logout/')
def logout():
    return "This page will process the oAuth logoff."

def MakeDictionary():
    categories = db_session.query(Category).all()
    finished_dict = []
    for c in categories:
        new_cat = c.serialize
        items = db_session.query(Item).filter_by(category_id = c.id).all()
        item_dict = []
        for i in items:
            item_dict.append(i.serialize)
        new_cat['Item'] = item_dict
        finished_dict.append(new_cat)
    return finished_dict

# implement Cross Site Request Forgery protection from flask_wtf
csrf = CsrfProtect()

@csrf.exempt
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = session.get('credentials')
    stored_gplus_id = session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    session['credentials'] = credentials.to_json()
    session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    session['username'] = data['name']
    session['picture'] = data['picture']
    session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += session['username']
    output += '!</h1>'
    output += '<img src="'
    output += session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % session['username'])
    print "done!"
    return output

if __name__ == '__main__':
    app.secret_key = '\r\x94b\xf3\xa5\xa5\x15\x13o\xa0DB\xa0m\x0e\xf1i\xa4"\xfeEW&W\xba\xc9Ko\x93'
    csrf.init_app(app)
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
