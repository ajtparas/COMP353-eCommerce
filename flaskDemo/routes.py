import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskDemo.models import User, Category, Order, Payment, Product, Shipper, Supply, OrderDetail, Supplier, getSupplier
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime


@app.route("/")
@app.route("/home")
def home():
    results2=Supplier.query.join(Supply,Supplier.SupplierID==Supply.SupplierID) \
               .add_columns(Supplier.ContactFname, Supplier.ContactLname, Supplier.SupplierID, Supply.SupplierID, Supply.ProductID) \
               .join(Product, Product.ProductID==Supply.ProductID).add_columns(Product.ProductName, Product.ProductID)
    results1=Supplier.query.join(Supply,Supplier.SupplierID==Supply.SupplierID) \
                .add_columns(Supplier.ContactFname, Supplier.ContactLname)
    return render_template('join.html', title='Join', joined_m_n=results2)

   

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(Username=form.username.data, Email=form.email.data, Password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(Email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.Password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))