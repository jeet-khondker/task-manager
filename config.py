import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Application Configurations
class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir, "app.db")
    
    # To disable feature of Flask-SQLAlchemy that is not needed
    # To signal the application every time a change is about to be made in DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email Configuration
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USER_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMINS = ["jeet.java.13@gmail.com"]

    # Supported Languages List
    LANGUAGES = ["en", "ja"]

    FLASK_ADMIN_SWATCH = "cerulean"