import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Application Configurations
class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir, "app.db")
    
    # To disable feature of Flask-SQLAlchemy that is not needed
    # To signal the application every time a change is about to be made in DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False