from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, ToDo

# Home Page URL Route
@app.route('/', methods = ["POST", "GET"])
@app.route("/index", methods = ["POST", "GET"])
@login_required
def index():
    if request.method == "POST":

        # Taking Form Data
        task_title = request.form["title"]
        task_description = request.form["description"]

        # Storing in ToDo Model
        new_task = ToDo(title = task_title, description = task_description)
        new_task.user_id = current_user.id

        # Adding In DB
        try:
            db.session.add(new_task)
            db.session.commit()
            flash("Your ToDo Item Successfully Created!")
            return redirect(url_for("index"))
        except:
            flash("There was an issue adding your task! Please try again later.")

    else:
        todoitems = ToDo.query.filter_by(user_id = current_user.id).order_by(ToDo.date_created.desc()).all()
        return render_template("index.html", todoitems = todoitems)

# User Login Form URL Route
@app.route("/login", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid Username Or Password")
            return redirect(url_for("login"))
        login_user(user, remember = form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", form = form)

# User Logout
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

# User Registration
@app.route("/register", methods = ["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations! You are now a registered user.")
        return redirect(url_for("login"))
    return render_template("register.html", form = form)