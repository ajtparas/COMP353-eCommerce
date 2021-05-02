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

    return render_template('home.html', title='Join')



@app.route("/supplierandproduct")
def supplierandproduct():
    results2=Supplier.query.join(Supply,Supplier.SupplierID==Supply.SupplierID) \
               .add_columns(Supplier.ContactFname, Supplier.ContactLname, Supplier.SupplierID, Supply.SupplierID, Supply.ProductID) \
               .join(Product, Product.ProductID==Supply.ProductID).add_columns(Product.ProductName, Product.ProductID)
    results1=Supplier.query.join(Supply,Supplier.SupplierID==Supply.SupplierID) \
                .add_columns(Supplier.ContactFname, Supplier.ContactLname)
    return render_template('supplierandproduct.html', title='Join', joined_m_n=results2)

 #all supplier related
@app.route("/supplier_home")
def supplier_home():
    results = Supplier.query.all()
    return render_template('supplier_home.html', outString = results)


@app.route("/supplier/<SupplierID>")
@login_required
def supplier(SupplierID):
    supplier = Supplier.query.get_or_404(SupplierID)
    return render_template('supplier.html', title=supplier.ContactFname, supplier=supplier, now=datetime.utcnow())


@app.route("/supplier/<SupplierID>/update", methods=['GET', 'POST'])
@login_required
def update_supplier(SupplierID):
    supplier = Supplier.query.get_or_404(SupplierID)
    currentSupplier = supplier.ContactFname

    form = SupplierUpdateForm()
    if form.validate_on_submit():          # notice we are are not passing the dnumber from the form
        if currentSupplier !=form.ContactFname.data:
            supplier.ContactFname=form.ContactFname.data
        supplier.ContactLname=form.ContactLname.data
        db.session.commit()
        flash('This supplier has been updated!', 'success')
        return redirect(url_for('supplier', SupplierID=SupplierID))
    elif request.method == 'GET':             
        form.SupplierID.data = supplier.SupplierID  # notice that we ARE passing the dnumber to the form
        form.ContactFname.data = supplier.ContactFname
        form.ContactLname.data = supplier.ContactLname
    return render_template('update_supplier.html', title='Update Supplier',
                           form=form, legend='Update Supplier') 

@app.route("/supplier/<SupplierID>/delete", methods=['POST'])
@login_required
def delete_supplier(SupplierID):
    supplier = Supplier.query.get_or_404(SupplierID)
    db.session.delete(supplier)
    db.session.commit()
    flash('This supplier been deleted!', 'success')
    return redirect(url_for('home'))


#admin register or login
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.Password.data).decode('utf-8')
        user = User(Username=form.Username.data, Email=form.Email.data, Password=hashed_password)
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
        user = User.query.filter_by(Email=form.Email.data).first()
        if user and bcrypt.check_password_hash(user.Password, form.Password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.Username = form.Username.data
        current_user.Email = form.Email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.Username.data = current_user.Username
        form.Email.data = current_user.Email
    return render_template('account.html', title='Account', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))