from flask_wtf import Form
from wtforms import TextField, SelectField, validators

# ### testing flask_wtf
# class MyForm(Form):
#     name = StringField('name', [validators.Length(min=4, max=25)])
# 
# 
# from wtforms import Form, 

class createItemForm(Form):
    title = TextField(u'Title', [validators.Length(min=4, max=250)])
    description = TextField(u'Description', [validators.Length(min=4, max=250)])
    image_url = TextField(u'Image URL', [validators.Length(min=4, max=250)])
    category = SelectField(u'Category', coerce=int)
