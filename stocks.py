from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt, check_password_hash

app = Flask(__name__) 
app.secret_key = 'teste'

bcrypt = Bcrypt(app)



app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{user}:{password}@{server}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        user = 'root',
        password = 'root',
        server = 'localhost',
        database = 'stock_market'
    )

db = SQLAlchemy(app)

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

@app.route('/')
def home():
    stock_list = Stocks.query.order_by(Stocks.id)
    print(stock_list)
    return render_template('home.html', stock_list=stock_list)

@app.route('/new_stock')
def new_stock():
    if session['user_log'] not in session or session['user_log'] == None:
        print("oi")
        return redirect(url_for('login', proxima=url_for('new_stock')))
    return render_template("new_stock.html")

@app.route('/create_stock', methods=['POST', ])
def create_stock():
    stock_list = Stocks.query.order_by(Stocks.id)
    company_name = request.form['company_name']
    ticket = request.form['ticket']
    price = request.form['price']
    market_cap = request.form['market_cap']

    stock = Stocks(company_name, ticket, price, market_cap)
    stock_list.append(stock)

    return redirect(url_for('home'))

@app.route('/login')
def login():
    next_page = request.args.get('next')
    return render_template("login.html", next=next_page)


@app.route('/autentification', methods=['POST', ])
def autentification():
    if 'username' in request.form and 'password' in request.form:
        user = Users.query.filter_by(nickname=request.form['username']).first()
        password = check_password_hash(user.password, request.form['password'])

    if user and password:
        session['user_log'] = user.nickname
        flash(user.nickname + ' login succeed.')
        next_page = request.form.get('next')
        if next_page:
            return redirect(next_page)
    else:
        flash('Login invalid!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['user_log'] == None
    flash('Logout succeed!')
    return redirect(url_for('home'))

app.run(debug=True)
