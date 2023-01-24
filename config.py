import os
SECRET_KEY = 'teste'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{user}:{password}@{server}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        user = 'root',
        password = 'root',
        server = 'localhost',
        database = 'stock_market'
    )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/static/uploads'