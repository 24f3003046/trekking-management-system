from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    #must mention this line, if you dont the class name will be considered as table name
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(15))
    role = db.Column(db.String(10), nullable=False, default="user")
    approved = db.Column(db.Boolean, default=True)
    blacklisted = db.Column(db.Boolean, default=False)
    joined_on = db.Column(db.DateTime, default=datetime.utcnow)

    #relationships
    assigned_treks = db.relationship("Trek", backref="staff", lazy=True)
    #check what this line is here please
    bookings = db.relationship( "Booking", backref="user", lazy=True,  cascade="all, delete-orphan")

    #for password hashing using werkzeug
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    #to check password during login
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    #not sure what this line here is
    def __repr__(self):
        return f"<User {self.username}>"


class Trek(db.Model):
    #must mention this line, if you dont the class name will be considered as table name
    __tablename__ = "treks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    altitude = db.Column(db.Integer)
    total_slots = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    #use default to have kind of a placeholder value
    status = db.Column(db.String(20), default="Pending")
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    staff_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    #relationships
    #check what this line is here please
    bookings = db.relationship("Booking", backref="trek",lazy=True, cascade="all, delete-orphan")

    #not sure what this line here is
    def __repr__(self):
        return f"<Trek {self.name}>"


class Booking(db.Model):
    #must mention this line, if you dont the class name will be considered as table name
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    booked_on = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="Booked")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey("treks.id"), nullable=False)

    def __repr__(self):
        return f"<Booking {self.id}>"