from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI

app = Flask(__name__) 
app.config.from_pyfile('config.py')


bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

from views import *

if  __name__ == '__main__':
    app.run(debug=True)
