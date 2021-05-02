from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import User, Category, Order, Payment, Product, Shipper, Supply, OrderDetail, Supplier, getSupplier
from wtforms.fields.html5 import DateField


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


#    mgr_start=DateField("Manager's Start Date", format='%Y-%m-%d')
      # This is using the html5 date picker (imported)
    submit = SubmitField('Update Supplier')


# got rid of def validate_dnumber

    def validate_ContactFname(self, ContactFname):    # apparently in the company DB, dname is specified as unique
         supplier = Supplier.query.filter_by(ContactFname=ContactFname.data).first()
         if supplier and (str(supplier.SupplierID) != str(self.SupplierID.data)):
             raise ValidationError('That department name is already being used. Please choose a different name.')


