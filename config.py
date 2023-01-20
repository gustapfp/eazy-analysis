SECRET_KEY = 'teste'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{user}:{password}@{server}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        user = 'root',
        password = 'root',
        server = 'localhost',
        database = 'stock_market'
    )