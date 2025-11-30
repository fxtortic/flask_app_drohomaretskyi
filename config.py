import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SECRET_KEY = "super_secret_key_123"
TEMPLATES_AUTO_RELOAD = True

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "app.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
