from main import db

class Stocks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(50), nullable=False)
    ticket = db.Column(db.String(8), nullable=False)
    price = db.Column(db.Float, nullable=False)
    market_cap = db.Column(db.Float, nullable=False)

    def __repr__(self) -> str:
        return '<Name %r>' % self.name

class Users(db.Model):
    name = db.Column(db.String(50), nullable=False)
    nickname = db.Column(db.String(8), primary_key=True)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return '<Name %r>' % self.name