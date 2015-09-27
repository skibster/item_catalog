from flask_wtf import Form
from wtforms import TextField, SelectField, validators
from flask_wtf.file import FileField

class createItemForm(Form):
    name = TextField(u'Item Name', [validators.Length(min=2, max=80)])
    description = TextField(u'Description', [validators.Length(min=2, max=250)])
    photo = FileField('Your photo')
    category = SelectField(u'Category', coerce=int)


class editItemForm(Form):
    name = TextField(u'Item Name', [validators.Length(min=2, max=80)])
    description = TextField(u'Description', [validators.Length(min=2, max=250)])
    photo = FileField('Your photo')
    category = SelectField(u'Category', coerce=int)
