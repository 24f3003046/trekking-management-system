from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, SelectField)
from wtforms.validators import ( DataRequired, Email, EqualTo, Length, ValidationError)

from models import User

#login form, creating only one for all 3 types of users
class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=30)]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )
    #what does this line do?
    submit = SubmitField("Login")

#form for new user to sign up/register
class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=30)]
    )

    name = StringField(
        "Full Name",
        validators=[DataRequired(), Length(max=100)]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    phone = StringField(
        "Phone Number",
        validators=[DataRequired(), Length(min=10, max=10)]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password")]
    )

    role = SelectField(
        "Register As",
        #why do we have 2 options for each? 
        choices=[("user", "User"), ("staff", "Staff")],
        validators=[DataRequired()]
    )

    #what does this line do?
    submit = SubmitField("Register")

    #username validation
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        #checks if username exists in db using db filtering
        if user:
            raise ValidationError(
                "Username already exists."
            )
    #email validation
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        #checks if email exists in db using db filtering
        if user:
            raise ValidationError(
                "Email already registered."
            )