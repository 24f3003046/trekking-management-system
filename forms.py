from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, SelectField)
from wtforms.validators import ( DataRequired, Email, EqualTo, Length, ValidationError)

from models import User

from wtforms import (
    TextAreaField,
    IntegerField,
    FloatField,
    DateField
)
from wtforms.validators import NumberRange, InputRequired

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
class TrekForm(FlaskForm):

    name = StringField(
        "Trek Name",
        validators=[DataRequired(), Length(max=100)]
    )

    location = StringField(
        "Location",
        validators=[DataRequired()]
    )

    difficulty = SelectField(
        "Difficulty",
        choices=[
            ("Easy", "Easy"),
            ("Moderate", "Moderate"),
            ("Hard", "Hard")
        ]
    )

    duration = IntegerField(
        "Duration (Days)",
        validators=[DataRequired(), NumberRange(min=1)]
    )

    description = TextAreaField("Description")

    price = FloatField(
        "Price",
        validators=[DataRequired(), NumberRange(min=0)]
    )

    altitude = IntegerField(
        "Altitude (m)",
        validators=[DataRequired(), NumberRange(min=0)]
    )

    total_slots = IntegerField(
        "Total Slots",
        validators=[DataRequired(), NumberRange(min=1)]
    )

    available_slots = IntegerField(
        "Available Slots",
        validators=[DataRequired(), NumberRange(min=0)]
    )

    status = SelectField(
        "Status",
        choices=[
            ("Pending", "Pending"),
            ("Open", "Open"),
            ("Closed", "Closed"),
        ]
    )

    start_date = DateField(
        "Start Date",
        format="%Y-%m-%d"
    )

    end_date = DateField(
        "End Date",
        format="%Y-%m-%d"
    )

    submit = SubmitField("Save Trek")


class AssignStaffForm(FlaskForm):

    staff = SelectField(
        "Assign Staff",
        coerce=int
    )

    submit = SubmitField("Assign")


class SearchForm(FlaskForm):

    keyword = StringField(
        "Search"
    )

    submit = SubmitField("Search")

class StaffUpdateTrekForm(FlaskForm):

    available_slots = IntegerField(
        "Available Slots",
        validators=[
            InputRequired(),
            NumberRange(min=0)
        ]
    )

    status = SelectField(
        "Status",
        choices=[
            ("Open", "Open"),
            ("Closed", "Closed"),
            ("Completed", "Completed")
        ]
    )

    submit = SubmitField("Update Trek")
class EditProfileForm(FlaskForm):

    name = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    phone = StringField(
        "Phone Number",
        validators=[
            DataRequired(),
            Length(min=10, max=15)
        ]
    )

    submit = SubmitField("Update Profile")