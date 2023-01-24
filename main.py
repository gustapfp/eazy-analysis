from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect



app = Flask(__name__) 
app.config.from_pyfile('config.py')


csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

from views import *

if  __name__ == '__main__':
    app.run(debug=True)
