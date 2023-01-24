from flask import render_template, request, redirect, url_for, session, flash, send_from_directory
from models import Stocks, Users
from flask_bcrypt import check_password_hash
from main import app, db
from helpers import return_image, delete_file, UsersForm, StockForm
import time

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
    form = StockForm()
    return render_template("new_stock.html", form=form)

@app.route('/create_stock', methods=['POST', ])
def create_stock():

    form = StockForm(request.form)
    if not form.validate_on_submit():
        return redirect(url_for('new_stock'))
    if form.validate_on_submit():
        company_name = form.company_name.data
        ticket = form.ticket.data
        price = form.price.data
        market_cap = form.market_cap.data

    stock = Stocks.query.filter_by(company_name=company_name).first()

    if stock:
        flash("Stock already register")

    stock = Stocks(company_name=company_name, ticket=ticket, price=price, market_cap=market_cap)
    db.session.add(stock)
    db.session.commit()

    company_logo = request.files['company_logo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    company_logo.save(f'{upload_path}/logo{stock.id}--{timestamp}.jpg')

    return redirect(url_for('home'))

@app.route('/edit_stock/<int:id>')
def edit_stock(id):
    if 'user_log' not in session or session['user_log'] == None:
        return redirect(url_for('login', next=url_for('update_stock')))
    stock = Stocks.query.filter_by(id=id).first()
    company_logo = return_image(id)
    form = StockForm()
    return render_template("update.html", stock=stock, company_logo=company_logo, form=form)

@app.route('/update_stock', methods=['POST',])
def update_stock():
    stock = Stocks.query.filter_by(id=request.form['id']).first()
    form = StockForm()
    form.company_name.data = stock.company_name 
    form.ticket.data = stock.ticket 
    form.price.data = stock.price 
    form.market_cap.data = stock.market_cap 

    db.session.add(stock)
    db.session.commit()

    image_file = request.files['company_logo']
    upload_path = app.config['UPLOAD_PATH']
    delete_file(id)
    timestamp = time.time()
    image_file.save(f'{upload_path}/logo{stock.id}--{timestamp}.jpg')

    return redirect(url_for('home'))

@app.route('/delete_stock/<int:id>')
def delete_stock(id):
    if 'user_log' not in session or session['user_log'] == None:
        return redirect(url_for('login'))

    Stocks.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Stock deleted.')

    return redirect(url_for('home'))

@app.route('/image/<file_name>')
def image(file_name):
    return send_from_directory('static/uploads/', file_name)


    

# User views

@app.route('/login')
def login():
    next_page = request.args.get('next')
    form = UsersForm()
    return render_template("login.html", next=next_page, form=form)


@app.route('/autentification', methods=['POST', ])
def autentification():
    
    user = Users.query.filter_by(nickname=request.form['nickname']).first()
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