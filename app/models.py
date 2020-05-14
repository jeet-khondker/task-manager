from datetime import datetime
from app import db, login, app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from time import time
import jwt


# Models Initialization & Definition
# User Model
class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    todoitems = db.relationship("ToDo", backref = "owner", lazy = "dynamic")

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in = 600):
        return jwt.encode(
            {"reset_password": self.id, "exp": time() + expires_in}, 
            app.config["SECRET_KEY"], algorithm = "HS256").decode("utf-8")

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config["SECRET_KEY"], algorithms = ["HS256"])["reset_password"]
        except:
            return
        return User.query.get(id)

# Loading A User
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# ToDo Model
class ToDo(db.Model):
    __tablename__ = "todoitems"

    item_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    date_updated = db.Column(db.DateTime)
    date_completed = db.Column(db.DateTime)
    is_completed = db.Column(db.Boolean, default = False, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)

    def __repr__(self):
        return "<Task {}>".format(self.title)

    def __init__(self, title, description):
        self.title = title
        self.description = description