import os
from main import app
from flask_wtf import FlaskForm
from wtforms  import StringField, SubmitField, PasswordField, FloatField, validators


def return_image(id):
    for file_name in os.listdir(app.config['UPLOAD_PATH']):
        if f'logo{id}' in file_name:
            return file_name
        return 'default_logo.png'

def delete_file(id):
    file = return_image(id)
    if file != 'default_logo.png':
        os.remove(os.path.join(app.config['UPLOAD_PATH']), file)


class StockForm(FlaskForm):
    company_name = StringField('Company name', [validators.DataRequired(), validators.Length(min=1, max=50)])
    ticket = StringField('Ticket', [validators.DataRequired(), validators.Length(min=4, max=8)])
    price = FloatField('Price', [validators.DataRequired()])
    market_cap = FloatField('Market Cap', [validators.DataRequired(),])
    save = SubmitField('Save')

class UsersForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired(), validators.Length(min=1, max=20)])
    nickname = StringField('Nickname', [validators.DataRequired(), validators.Length(min=1, max=8)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=4, max=100)])
    login = SubmitField('Login')
