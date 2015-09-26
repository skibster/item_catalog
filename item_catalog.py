"""item_catalog.py generates a Python Flask website for Udacity's Full Stack Web Developer Nanodegree Project 3"""

import os, json
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, session

from flask_wtf.csrf import CsrfProtect
from wt_form_functions import createItemForm, editItemForm
from werkzeug import secure_filename

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
@app.route('/catalog')
def showCatalog():
    categories = db_session.query(Category).order_by(asc(Category.name))
    last_items = db_session.query(Item, Category).filter(Item.category_id==Category.id).order_by(desc(Item.last_updated)).limit(10)
    return render_template('showCatalog.html', categories=categories, last_items=last_items )

"""This route is the root of the web application and returns the catalog categories and top ten recent items."""
@app.route('/')
@app.route('/catalog/json')
def jsonCatalog():
    items = db_session.query(Category, Item).filter(Item.category_id==Category.id).all()
    return jsonify(Category=[c.serialize for c, i in items], Item=[i.serialize for c, i in items])
    
    # def row2dict(row):
    #     d = {}
    #     for column in row.__table__.columns:
    #       d[column.name] = str(getattr(row, column.name))
    #     return d
    # 
    # finished_dict = []
    # for c in db_session.query(Category).filter_by(id=3).all():
    #     category_dict = ( row2dict(c) )
    #     print category_dict
    #     item_dict = []
    #     for i in db_session.query(Item).filter_by(category_id=c.id).all():
    #         item_dict.append( row2dict(i))
    #     finished_dict.append(["Category", category_dict, ["Item", item_dict]])
    # return json.dumps(finished_dict)


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
        image_url='static/blank.png'
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
        flash('New item: %s has been created.' % newItem.name)
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
            os.remove(old_image)
            image_dir = 'static/uploads/%s/' % item.id
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
        return redirect(url_for('showCategory', category_name=category.name))
    return render_template('editItem.html', form=form, item=item, item_name=item_name, category_name=category.name)

"""This route allows a user to delete a specific item they created."""
@app.route('/catalog/<string:item_name>/delete', methods=['GET', 'POST'])
def deleteItem(item_name):
    item = db_session.query(Item).filter_by(name=item_name).one()
    category = db_session.query(Category).filter_by(id=item.category_id).one()

    if request.method == 'POST':
        os.remove(item.image_url)
        old_dir = 'static/uploads/%s/' % item.id
        os.removedirs(old_dir)
        db_session.delete(item)
        db_session.commit()
        flash('Your item has been deleted.')
        return redirect(url_for('showCategory', category_name=category.name))
    return render_template('deleteItem.html', item_name=item_name, category_name=category.name)

"""This route shows details about a single item."""
@app.route('/catalog/<string:category_name>/<string:item_name>', methods=['GET'])
def showItem(category_name, item_name):
    item = db_session.query(Item).filter_by(name=item_name).one()
    return render_template('showItem.html', item=item, category_name=category_name)

"""This route handles logging in the user using the Google OAuth API."""
@app.route('/catalog/login')
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
