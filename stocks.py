from flask import Flask, render_template

app = Flask(__name__)


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
        

@app.route('/')
def home():
    return render_template('home.html', stock_list=stock_list)

@app.route('/new_stock')
def new_stock():
    return render_template("new_stock.html")



app.run(debug=True)