from flask import Flask, render_template, request, redirect, url_for, session, flash




class Stock:
    def __init__(self, company_name, ticket, price, market_cap) -> None:
        self.company_name = company_name
        self.ticket = ticket
        self.price = price
        self.market_cap = market_cap

class User:
    def __init__(self, name, nickname, password):
        self.name = name
        self.nickname = nickname
        self.password = password




itub4 = Stock('Itaú Unibanco', 'ITUB4', 25.87, 238.03)
bbdc4 =  Stock('Bradesco', 'BBDC4', 15.19, 152.37 )
nubr33 = Stock('Nu Holdings Ltd', 'NUBR33', 3.10, 86.73)
stock_list = [itub4, bbdc4, nubr33]

user1 = User('Gustavo', 'gustapfp', '1234')
user2 = User('Maria','mary', '1234')

users_list = {
    user1.nickname:user1,
    user2.nickname:user2
}
        
app = Flask(__name__) 
app.secret_key = 'teste'

app.config['SQLACHEMY_DATABASE_URI'] = '{SGBD}://{user}:{password}@{server}/database'.format(
    SGBD = 'mysql+mysqlconnector',
    usuario = 'root',
    senha = 'admin',
    servidor = 'localhost',
    database = 'jogoteca'
)



@app.route('/')
def home():
    return render_template('home.html', stock_list=stock_list)

@app.route('/new_stock')
def new_stock():
    if session['user_log'] not in session or session['user_log'] == None:
        print("oi")
        return redirect(url_for('login', proxima=url_for('new_stock')))
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
    next_page = request.args.get('next')
    return render_template("login.html", next=next_page)


@app.route('/autentification', methods=['POST', ])
def autentification():
    username = request.form['username']
    password = request.form['password']

    if username in users_list:
        user = users_list[username]
        if password == users_list[username].password:
            session['user_log'] = user.nickname
            flash(user.nickname + ' login succeed.')
            next_page = request.form['next']
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