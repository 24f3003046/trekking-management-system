import os
# To prevent circular imports, using config to allow models.py and app.py to access db
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = "trekinerary-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "instance", "trekinerary.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False