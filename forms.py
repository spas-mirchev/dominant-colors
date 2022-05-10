from flask_wtf import FlaskForm
from wtforms import FileField, IntegerField
from wtforms.fields import html5 as h5fields
from wtforms.widgets import html5 as h5widgets

class FormUpload(FlaskForm):
    image = FileField('image')
    number_of_colors = h5fields.IntegerField(default=5)
    delta = h5fields.IntegerField(default=5)  
