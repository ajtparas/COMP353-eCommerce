from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import User, Category, Order, Payment, Product, Shipper, Supply, OrderDetail, Supplier, getSupplier
from wtforms.fields.html5 import DateField


#  or could have used ssns = db.session.query(Department.mgr_ssn).distinct()
# for that way, we would have imported db from flaskDemo, see above
sup=Supplier.query.with_entities(Supplier.SupplierID).distinct()#Creating drop down for Employee
results1=list()
for row in sup:
    rowDict=row._asdict()
    results1.append(rowDict)
supChoice=[(row['SupplierID'],row['SupplierID']) for row in results1]

pro=Product.query.with_entities(Product.ProductID).distinct()
results2=list()#Creating drop down for Projects
for row in pro:
    rowDict=row._asdict()
    results2.append(rowDict)
product=[(row['ProductID'],row['ProductID']) for row in results2]


cat=Category.query.with_entities(Category.CategoryID).distinct()#Creating drop down for Employee
results1=list()
for row in cat:
    rowDict=row._asdict()
    results1.append(rowDict)
catChoice=[(row['CategoryID'],row['CategoryID']) for row in results1]



class RegistrationForm(FlaskForm):
    Username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    Email = StringField('Email',
                        validators=[DataRequired(), Email()])
    Password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('Password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, Username):
        user = User.query.filter_by(Username=Username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, Email):
        user = User.query.filter_by(Email=Email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    Email = StringField('Email',
                        validators=[DataRequired(), Email()])
    Password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    Username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    Email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, Username):
        if Username.data != current_user.Username:
            user = User.query.filter_by(Username=Username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, Email):
        if email.data != current_user.Email:
            user = User.query.filter_by(Email=Email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


#all supplier related
class SupplierUpdateForm(FlaskForm):


    SupplierID = HiddenField("")

    ContactFname=StringField('Supplier First Name:', validators=[DataRequired(),Length(max=15)])
    ContactLname=StringField('Supplier Last Name:', validators=[DataRequired(),Length(max=15)])
    submit = SubmitField('Update Supplier')

    def validate_ContactFname(self, ContactFname):    # apparently in the company DB, dname is specified as unique
         supplier = Supplier.query.filter_by(ContactFname=ContactFname.data).first()
         if supplier and (str(supplier.SupplierID) != str(self.SupplierID.data)):
             raise ValidationError('That supplier name is already being used. Please choose a different name.')


class SupplierForm(SupplierUpdateForm):

    SupplierID=IntegerField('Supplier ID', validators=[DataRequired()])
    submit = SubmitField('Add Supplier')

    def validate_dnumber(self, SupplierID):    #because dnumber is primary key and should be unique
        supplier = Supplier.query.filter_by(SupplierID=SupplierID.data).first()
        if supplier:
            raise ValidationError('Supplier ID is taken. Please choose a different one.')


#all product related
class ProductUpdateForm(FlaskForm):


    ProductID = HiddenField("")

    ProductName=StringField('Product Name:', validators=[DataRequired(),Length(max=15)])
    CategoryID=SelectField('Category ID:', choices=catChoice, validators=[DataRequired(),Length(max=15)])
    submit = SubmitField('Update Product')

    def validate_ProductName(self, ProductName):    # apparently in the company DB, dname is specified as unique
         product = Product.query.filter_by(ProductName=ProductName.data).first()
         if product and (str(product.ProductID) != str(self.ProductID.data)):
             raise ValidationError('That product name is already being used. Please choose a different name.')


class ProductForm(ProductUpdateForm):

    ProductID=IntegerField('Product ID', validators=[DataRequired()])
    CategoryID=SelectField('Category ID', choices=catChoice, validators=[DataRequired()])
    submit = SubmitField('Add Product')

    def validate_dnumber(self, ProductID):    #because dnumber is primary key and should be unique
        product = Product.query.filter_by(ProductID=ProductID.data).first()
        if product:
            raise ValidationError('ProductID is taken. Please choose a different one.')

#all payment related
class PaymentUpdateForm(FlaskForm):


    PaymentID = HiddenField("")
    PaymentType=StringField('Payment Type:', validators=[DataRequired(),Length(max=15)])
    submit = SubmitField('Update Payment')

    def validate_PaymentType(self, PaymentType):    # apparently in the company DB, dname is specified as unique
         payment = Payment.query.filter_by(PaymentType=PaymentType.data).first()
         if payment and (str(payment.PaymentID) != str(self.PaymentID.data)):
             raise ValidationError('That payment type is already being used. Please choose a different name.')



class PaymentForm(PaymentUpdateForm):

    PaymentID=IntegerField('Payment ID', validators=[DataRequired()])
    submit = SubmitField('Add Payment')

    def validate_dnumber(self, PaymentID):    #because dnumber is primary key and should be unique
        payment = Payment.query.filter_by(PaymentID=PaymentID.data).first()
        if payment:
            raise ValidationError('Payment ID is taken. Please choose a different one.')

#all category related
class CategoryUpdateForm(FlaskForm):


    CategoryID = HiddenField("")
    CategoryName=StringField('Category Name:', validators=[DataRequired(),Length(max=15)])
    Description=StringField('Description:', validators=[DataRequired(),Length(max=15)])
    submit = SubmitField('Category Update')

    def validate_CategoryName(self, CategoryName):    # apparently in the company DB, dname is specified as unique
         category = Category.query.filter_by(CategoryName=CategoryName.data).first()
         if category and (str(category.CategoryID) != str(self.CategoryID.data)):
             raise ValidationError('That category is already being used. Please choose a different name.')



class CategoryForm(CategoryUpdateForm):

    CategoryID=IntegerField('Category ID', validators=[DataRequired()])
    submit = SubmitField('Add Category')

    def validate_dnumber(self, CategoryID):    #because dnumber is primary key and should be unique
        category = Category.query.filter_by(CategoryID=CategoryID.data).first()
        if category:
            raise ValidationError('Category ID is taken. Please choose a different one.')



class AssignForm(FlaskForm):
    SupplierID=SelectField("Supplier", choices=supChoice)
    ProductID=SelectField("Product", choices=product, coerce=int)
    submit=SubmitField("Assign")

    def validate_SupplierID(self, SupplierID):
        pairs=Supply.query.filter_by(ProductID=self.ProductID.data)
        if pairs:
            for pair in pairs:
                if str(pair.SupplierID)==str(self.SupplierID.data):
                    raise ValidationError('That Supplier has already been assigned to that product.')

