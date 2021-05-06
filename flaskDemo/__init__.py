from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1:8889/eCommerce'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'



r = db.engine.execute('select ShipperID, CompanyPhone from Shippers where\
	CompanyName="Adidas" and CompanyRep="Justin"')

names = [row for row in r]

print(names)



q = db.engine.execute('select Orders.OrderID, Shippers.ShipperID,\
 Orders.OrderNumber from Orders inner join\
	Shippers on Orders.ShipperID=Shippers.ShipperID')

tnames = [row for row in q]

print(tnames)




w = db.engine.execute('select OrderNumber from Orders where CustomerID\
	in (select CustomerID from Orders where PaymentID="21112")')
wnames = [row for row in w]

print(wnames)

from flaskDemo import routes
from flaskDemo import models

models.db.create_all()
