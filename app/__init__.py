from flask import Flask, url_for, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l

import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

app = Flask(__name__)

app.config.from_object(Config)

# Database Initialization
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Adding Admin I/F for user list
admin = Admin(app)

login = LoginManager(app)
login.login_view = "login"
login.login_message = _l("Please login to access the system.")

bootstrap = Bootstrap(app)

mail = Mail(app)

moment = Moment(app)

babel = Babel(app)

from app import routes, models, errors

# Adding Admin I/F for user list
admin.add_view(ModelView(models.User, db.session))

# Logging Errors By Email
if not app.debug:
    if app.config["MAIL_SERVER"]:
        auth = None

        if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
            auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])

        secure = None

        if app.config["MAIL_USE_TLS"]:
            secure = ()

        mail_handler = SMTPHandler(
            mailhost = (app.config["MAIL_SERVER"], app.config["MAIL_PORT"]), 
            fromaddr = "no-reply@" + app.config["MAIL_SERVER"], 
            toaddrs = app.config["ADMINS"], subject = "System Failure Issue", 
            credentials = auth, secure = secure
        )

        mail_handler.setLevel(logging.ERROR)
        
        app.logger.addHandler(mail_handler)

        if not os.path.exists("logs"):
            os.mkdir("logs")
        file_handler = RotatingFileHandler("logs/execution.log", maxBytes = 10240, backupCount = 10)
        file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("Application StartUp")

# Selecting the best language
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config["LANGUAGES"])


