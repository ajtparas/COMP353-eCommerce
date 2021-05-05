from datetime import datetime
from flaskDemo import db, login_manager
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship

db.Model.metadata.reflect(db.engine)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(20), unique=True, nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Password = db.Column(db.String(60), nullable=False)

    def get_id(self):
           return (self.UserID)

    def __repr__(self):
        return f"User('{self.Username}', '{self.Email}')"




class Category(db.Model):
    __table__ = db.Model.metadata.tables['Category']
    
class Order(db.Model):
    __table__ = db.Model.metadata.tables['Orders']



class Payment(db.Model):
    __table__ = db.Model.metadata.tables['Payment']
    
    
class Product(db.Model):
    __table__ = db.Model.metadata.tables['Products']
class Shipper(db.Model):
    __table__ = db.Model.metadata.tables['Shippers']
class Supply(db.Model):
    __table__ = db.Model.metadata.tables['Supply']




class OrderDetail(db.Model):
    __table__ = db.Model.metadata.tables['OrderDetails']

class Supplier(db.Model):
    __table__ = db.Model.metadata.tables['Suppliers']
   


def getSupplier(columns=None):
    u = Supplier.query
    if columns:
        u = u.options(orm.load_only(*columns))
    return u





    

  
