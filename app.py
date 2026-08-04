import os

from flask import Flask

#to connect db
from config import Config
from extensions import db, login_manager

#import models so sqlalchemy knows them
from models import User

#using blueprints to make access to each code part of app easy to access
from app_routes.auth import auth_bp
from app_routes.admin import admin_bp
from app_routes.staff import staff_bp
from app_routes.user import user_bp


#creates the flask app
app = Flask(__name__)

#instead of app.config["SECRET_KEY"] = ... everywhere we do this, also easy to convert to mysql or postgres
app.config.from_object(Config)

#initialize app in flask..?
db.init_app(app)
login_manager.init_app(app)


#register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(staff_bp, url_prefix="/staff")
app.register_blueprint(user_bp)

#to create the admin
#why are we not creating others? oh its mentoned in requirements to pre-create an admin (hard code)
def create_admin():
    admin = User.query.filter_by(username="admin").first()
    #hard-coding the admin
    if not admin:
        admin = User(
            username="admin",
            name="Administrator",
            email="admin@trekinerary.com",
            phone="0000000000",
            role="admin",
            approved=True
        )
        #admin password, don't forget
        admin.set_password("admin123")

        #creating session for admin(user)
        db.session.add(admin)
        db.session.commit()
        print("Default Admin Created")

#what's this?
with app.app_context():
    if not os.path.exists("instance"):
        os.makedirs("instance")

    db.create_all()
    create_admin()

#setting url pattern 
@app.route("/")

#temporary, to check if app running
def home():
    return "<h1>Welcome to Trekinerary</h1>"


if __name__ == "__main__":
    app.run(debug=True)