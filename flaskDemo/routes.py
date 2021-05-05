import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, SupplierUpdateForm, SupplierForm, ProductUpdateForm, ProductForm, PaymentUpdateForm, PaymentForm, CategoryUpdateForm, CategoryForm, AssignForm
from flaskDemo.models import User, Category, Order, Payment, Product, Shipper, Supply, OrderDetail, Supplier, getSupplier
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime


@app.route("/")
def no_admin():
    return render_template('noadmin.html', title='Join')



@app.route("/")
@app.route("/home")
@login_required
def home():
    return render_template('home.html', title='Join')


#all supplier and product related
@app.route("/supplierandproduct")
@login_required
def supplierandproduct():
    results2=Supplier.query.join(Supply,Supplier.SupplierID==Supply.SupplierID) \
               .add_columns(Supplier.ContactFname, Supplier.ContactLname, Supplier.SupplierID, Supply.SupplierID, Supply.ProductID) \
               .join(Product, Product.ProductID==Supply.ProductID).add_columns(Product.ProductName, Product.ProductID)
    results1=Supplier.query.join(Supply,Supplier.SupplierID==Supply.SupplierID) \
                .add_columns(Supplier.ContactFname, Supplier.ContactLname)
    return render_template('supplierandproduct.html', title='Join', joined_m_n=results2)


@app.route("/assign/<ProductID>/<SupplierID>")
@login_required
def assign(SupplierID, ProductID):
    assign = Supply.query.get_or_404([SupplierID,ProductID])
    return render_template('assign.html', title=str(assign.SupplierID)+"_"+str(assign.ProductID), assign=assign, now=datetime.utcnow)

@app.route("/assign/<ProductID>/<SupplierID>/delete", methods=['POST'])
@login_required
def delete_assignment(SupplierID,ProductID):
    assign = Supply.query.get_or_404([SupplierID,ProductID])
    db.session.delete(assign)
    db.session.commit()
    flash('The assignment has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/assign/new", methods=['GET', 'POST'])
@login_required
def new_assign():
    form = AssignForm()
    if form.validate_on_submit():
        assign = Supply(SupplierID=form.SupplierID.data, ProductID=form.ProductID.data)
        db.session.add(assign)
        db.session.commit()
        flash('You have assigned a supplier!', 'success')
        return redirect(url_for('home'))
    return render_template('create_supply.html', title='Assign a Supplier',
                           form=form, legend='Assign Supplier')






 #all supplier related
@app.route("/supplier_home")
@login_required
def supplier_home():
    results = Supplier.query.all()
    return render_template('supplier_home.html', outString = results)


@app.route("/supplier/new", methods=['GET', 'POST'])
@login_required
def new_supplier():
    form = SupplierForm()
    if form.validate_on_submit():
        supplier = Supplier(ContactFname=form.ContactFname.data, SupplierID=form.SupplierID.data,ContactLname=form.ContactLname.data)
        db.session.add(supplier)
        db.session.commit()
        flash('You have added a new supplier!', 'success')
        return redirect(url_for('home'))
    return render_template('create_supplier.html', title='New Supplier',
                           form=form, legend='New Supplier')


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


#all product related
@app.route("/product_home")
@login_required
def product_home():
    results = Product.query.all()
    return render_template('product_home.html', outString = results)

@app.route("/product/<ProductID>")
@login_required
def product(ProductID):
    product = Product.query.get_or_404(ProductID)
    return render_template('product.html', title=product.ProductName, product=product, now=datetime.utcnow())


@app.route("/product/<ProductID>/update", methods=['GET', 'POST'])
@login_required
def update_product(ProductID):
    product = Product.query.get_or_404(ProductID)
    currentProduct = product.ProductName

    form = ProductUpdateForm()
    if form.validate_on_submit():          # notice we are are not passing the dnumber from the form
        if currentProduct !=form.ProductName.data:
            product.ProductName=form.ProductName.data
        product.CategoryID=form.CategoryID.data
        db.session.commit()
        flash('This product has been updated!', 'success')
        return redirect(url_for('product', ProductID=ProductID))
    elif request.method == 'GET':             
        form.ProductID.data = product.ProductID  # notice that we ARE passing the dnumber to the form
        form.ProductName.data = product.ProductName
        form.CategoryID.data = product.CategoryID
    return render_template('update_product.html', title='Update Product',
                           form=form, legend='Update Product') 

@app.route("/product/<ProductID>/delete", methods=['POST'])
@login_required
def delete_product(ProductID):
    product = Product.query.get_or_404(ProductID)
    db.session.delete(product)
    db.session.commit()
    flash('This product been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/product/new", methods=['GET', 'POST'])
@login_required
def new_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(ProductName=form.ProductName.data, ProductID=form.ProductID.data,CategoryID=form.CategoryID.data)
        db.session.add(product)
        db.session.commit()
        flash('You have added a new product!', 'success')
        return redirect(url_for('home'))
    return render_template('create_product.html', title='New Product',
                           form=form, legend='New Product')


#all payment related
@app.route("/payment_home")
def payment_home():
    results = Payment.query.all()
    return render_template('payment_home.html', outString = results)


@app.route("/payment/<PaymentID>")
@login_required
def payment(PaymentID):
    payment = Payment.query.get_or_404(PaymentID)
    return render_template('payment.html', title=payment.PaymentType, payment=payment, now=datetime.utcnow())


@app.route("/payment/<PaymentID>/update", methods=['GET', 'POST'])
@login_required
def update_payment(PaymentID):
    payment = Payment.query.get_or_404(PaymentID)
    currentPayment = payment.PaymentType

    form = PaymentUpdateForm()
    if form.validate_on_submit():          # notice we are are not passing the dnumber from the form
        if currentPayment !=form.PaymentType.data:
            payment.PaymentID=form.PaymentType.data
        db.session.commit()
        flash('This payment has been updated!', 'success')
        return redirect(url_for('payment', PaymentID=PaymentID))
    elif request.method == 'GET':             
        form.PaymentID.data = payment.PaymentID  # notice that we ARE passing the dnumber to the form
        form.PaymentType.data = payment.PaymentType
    return render_template('update_payment.html', title='Update Payment',
                           form=form, legend='Update Payment') 

@app.route("/payment/<PaymentID>/delete", methods=['POST'])
@login_required
def delete_payment(PaymentID):
    payment = Payment.query.get_or_404(PaymentID)
    db.session.delete(payment)
    db.session.commit()
    flash('This payment been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/payment/new", methods=['GET', 'POST'])
@login_required
def new_payment():
    form = PaymentForm()
    if form.validate_on_submit():
        payment = Payment(PaymentType=form.PaymentType.data, PaymentID=form.PaymentID.data)
        db.session.add(payment)
        db.session.commit()
        flash('You have added a new payment!', 'success')
        return redirect(url_for('home'))
    return render_template('create_payment.html', title='New Payment',
                           form=form, legend='New Payment')



#all category related
@app.route("/category_home")
def category_home():
    results = Category.query.all()
    return render_template('category_home.html', outString = results)


@app.route("/category/<CategoryID>")
@login_required
def category(CategoryID):
    category = Category.query.get_or_404(CategoryID)
    return render_template('category.html', title=category.CategoryName, category=category, now=datetime.utcnow())




@app.route("/category/<CategoryID>/update", methods=['GET', 'POST'])
@login_required
def update_category(CategoryID):
    category = Category.query.get_or_404(CategoryID)
    currentCategory = category.CategoryName

    form = CategoryUpdateForm()
    if form.validate_on_submit():          # notice we are are not passing the dnumber from the form
        if currentCategory !=form.CategoryName.data:
            category.CategoryName=form.CategoryName.data
        category.Description=form.Description.data
        db.session.commit()
        flash('This category has been updated!', 'success')
        return redirect(url_for('category', CategoryID=CategoryID))
    elif request.method == 'GET':             
        form.CategoryID.data = category.CategoryID  # notice that we ARE passing the dnumber to the form
        form.CategoryName.data = category.CategoryName
        form.Description.data = category.Description
    return render_template('update_category.html', title='Update Category',
                           form=form, egend='Update Category') 

@app.route("/category/<CategoryID>/delete", methods=['POST'])
@login_required
def delete_category(CategoryID):
    category = Category.query.get_or_404(CategoryID)
    db.session.delete(category)
    db.session.commit()
    flash('This category been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/category/new", methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(CategoryName=form.CategoryName.data, CategoryID=form.CategoryID.data, Description=form.Description.data)
        db.session.add(category)
        db.session.commit()
        flash('You have added a new category!', 'success')
        return redirect(url_for('home'))
    return render_template('create_category.html', title='New Category',
                           form=form, legend='New Category')



#all order related
@app.route("/order_home")
@login_required
def order_home():
    results = Order.query.all()
    return render_template('order_home.html', outString = results)

@app.route("/order/<OrderID>")
@login_required
def order(OrderID):
    order = OrderDetail.query.get_or_404(OrderID,ProductID)
    return render_template('order.html', title=order.CustomerID, order=order, now=datetime.utcnow())



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