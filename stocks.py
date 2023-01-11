from flask import Flask, render_template, request, redirect, url_for




class Stock:
    def __init__(self, company_name, ticket, price, market_cap) -> None:
        self.company_name = company_name
        self.ticket = ticket
        self.price = price
        self.market_cap = market_cap




itub4 = Stock('Itaú Unibanco', 'ITUB4', 25.87, 238.03)
bbdc4 =  Stock('Bradesco', 'BBDC4', 15.19, 152.37 )
nubr33 = Stock('Nu Holdings Ltd', 'NUBR33', 3.10, 86.73)
stock_list = [itub4, bbdc4, nubr33]
        
app = Flask(__name__) 

@app.route('/')
def home():
    return render_template('home.html', stock_list=stock_list)

@app.route('/new_stock')
def new_stock():
    return render_template("new_stock.html")

@app.route('/create_stock', methods=['POST', ])
def create_stock():
    company_name = request.form['company_name']
    ticket = request.form['ticket']
    price = request.form['price']
    market_cap = request.form['market_cap']

    stock = Stock(company_name, ticket, price, market_cap)
    stock_list.append(stock)

    return redirect(url_for('home'))

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/autentification', methods=['POST', ])
def autentification():
    username = request.form['username']
    password = request.form['password']

    if username == 'guga' and password == 'teste':
        return redirect(url_for('home'))
        
    return redirect('/login')



app.run(debug=True)