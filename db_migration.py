import mysql.connector 
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash


try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='root'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `stock_market`;")

cursor.execute("CREATE DATABASE `stock_market`;")

cursor.execute("USE `stock_market`;")

# criando tabelas
TABLES = {}
TABLES['Stocks'] = ('''
      CREATE TABLE `stocks` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `company_name` varchar(50) NOT NULL,
      `price` DOUBLE NOT NULL,
      `market_cap` DOUBLE NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Users'] = ('''
      CREATE TABLE `users` (
      `name` varchar(20) NOT NULL,
      `nickname` varchar(8) NOT NULL,
      `password` varchar(100) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for table_name in TABLES:
      table_sql = TABLES[table_name]
      try:
            print('Creating table {}:'.format(table_name), end=' ')
            cursor.execute(table_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Already exists')
            else:
                  print(err.msg)
      else:
            print('OK')


# inserindo usuarios
user_sql = 'INSERT INTO users (name, nickname, password) VALUES (%s, %s, %s)'
user = [
      ("Bruno Divino", "BD", generate_password_hash("12345678").decode('utf-8')),
      ("Camila Ferreira", "Mila", generate_password_hash("87654321").decode('utf-8')),
      ("Guilherme Louro", "Cake", generate_password_hash("12344321").decode('utf-8'))
]
cursor.executemany(user_sql, user)

cursor.execute('select * from stock_market.users')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
stocks_sql = 'INSERT INTO jogos (company_name, price, market_cap) VALUES (%s, %s, %s)'
stocks = [
      ('Itaú Unibanco', 'ITUB4', 25.87, 238.03),
      ('Bradesco', 'BBDC4', 15.19, 152.37 ),
      ('Nu Holdings Ltd', 'NUBR33', 3.10, 86.73),
]
cursor.executemany(stocks_sql, stocks)

cursor.execute('select * from stock_market.stocks')
print(' -------------  Stocks:  -------------')
for stock in cursor.fetchall():
    print(stock[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()