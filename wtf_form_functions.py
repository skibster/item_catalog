from flask_wtf import Form
from wtforms import TextField, SelectField, validators

class createItemForm(Form):
    name = TextField(u'Item Name', [validators.Length(min=4, max=250)])
    description = TextField(u'Description', [validators.Length(min=4, max=250)])
    image_url = TextField(u'Image URL', [validators.Length(min=4, max=250)])
    category = SelectField(u'Category', coerce=int)


class editItemForm(Form):
    name = TextField(u'Item Name', [validators.Length(min=4, max=250)])
    description = TextField(u'Description', [validators.Length(min=4, max=250)])
    image_url = TextField(u'Image URL', [validators.Length(min=4, max=250)])
    category = SelectField(u'Category', coerce=int)
