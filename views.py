from flask import render_template, request, redirect, url_for, session, flash
from models import Stocks, Users
from flask_bcrypt import check_password_hash
from main import app, db


# app views:

@app.route('/')
def home():
    stock_list = Stocks.query.order_by(Stocks.id)
    print(stock_list)
    return render_template('home.html', stock_list=stock_list)

@app.route('/new_stock')
def new_stock():
    if 'user_log' not in session or session['user_log'] == None:
        return redirect(url_for('login', next=url_for('new_stock')))
    return render_template("new_stock.html")

@app.route('/create_stock', methods=['POST', ])
def create_stock():
    company_name = request.form['company_name']
    ticket = request.form['ticket']
    price = request.form['price']
    market_cap = request.form['market_cap']

    stock = Stocks.query.filter_by(company_name=company_name).first()

    if stock:
        flash("Stock already register")

    stock = Stocks(company_name=company_name, ticket=ticket, price=price, market_cap=market_cap)
    db.session.add(stock)
    db.session.commit()

    return redirect(url_for('home'))

@app.route('/edit_stock/<int:id>')
def edit_stock(id):
    if 'user_log' not in session or session['user_log'] == None:
        return redirect(url_for('login', next=url_for('update_stock')))
    stock = Stocks.query.filter_by(id=id).first()
    return render_template("update.html", stock=stock)

@app.route('/update_stock', methods=['POST',])
def update_stock():
    stock = Stocks.query.filter_by(id=request.form['id']).first()
    stock.company_name = request.form['company_name']
    stock.ticket = request.form['ticket']
    stock.price = request.form['price']
    stock.market_cap = request.form['market_cap']

    db.session.add(stock)
    db.session.commit()

    return redirect(url_for('home'))

@app.route('/delete_stock/<int:id>')
def delete_stock(id):
    if 'user_log' not in session or session['user_log'] == None:
        return redirect(url_for('login'))

    Stocks.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Stock deleted.')

    return redirect(url_for('home'))

    

# User views

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
        next_page = request.form['next']
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