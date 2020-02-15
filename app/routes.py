from flask import render_template, url_for, flash, redirect, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User, ToDo

from datetime import datetime

# Home Page URL Route
@app.route('/', methods = ["POST", "GET"])
@app.route("/index", methods = ["POST", "GET"])
@login_required
def index():
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

# Add Task
@app.route("/add", methods = ["POST"])
def add_task():
    if request.method == "POST":
        # Taking Form Data To Add A Task
        task_title = request.form["title"]
        task_description = request.form["description"]

        # Storing Data In ToDo Model
        new_task = ToDo(title = task_title, description = task_description)
        new_task.user_id = current_user.id
        new_task.is_completed = False

        # Adding In DB
        try:
            db.session.add(new_task)
            db.session.commit()
            flash("Item Added! Your ToDo Item Successfully Created!")
            return redirect(url_for("index"))
        except:
            flash("There was an issue adding your task! Please try again later.")

# Update Task
@app.route("/update", methods = ["GET", "POST"])
def update():
    if request.method == "POST":
        task = ToDo.query.get(request.form.get("item_id"))
        task.title = request.form["title"]
        task.description = request.form["description"]
        task.date_updated = datetime.utcnow()

        db.session.commit()
        flash("Task Item Updated Successfully.")
        return redirect(url_for("index"))

# ToDo Item Deletion
@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = ToDo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for("index"))
    except:
        flash("There was an problem deleting that task! Please try again later.")

# User Profile View
@app.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username = username).first_or_404()
    return render_template("user.html", user = user)

# Edit User Profile Information
@app.route("/editProfile", methods = ["GET", "POST"])
@login_required
def editProfile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.firstName = form.firstName.data
        current_user.lastName = form.lastName.data
        db.session.commit()
        flash("Your changes have been saved")
        return redirect(url_for("editProfile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.firstName.data = current_user.firstName
        form.lastName.data = current_user.lastName
    return render_template("editProfile.html", form = form)

# Marking Task As Complete
@app.route("/done/<int:id>")
@login_required
def done_task(id):
    task_completed = ToDo.query.get_or_404(id)
    task_completed.is_completed = True
    task_completed.date_completed = datetime.utcnow()
    
    db.session.commit()

    tasks = ToDo.query.all()

    return redirect(url_for("index"))

# Task Report - Summarizing All The Completed Tasks
@app.route("/taskreport/<username>")
@login_required
def view_taskreport(username):
    completed_todoitems = ToDo.query.filter_by(user_id = current_user.id and ToDo.is_completed == True).order_by(ToDo.date_created.desc()).all()
    return render_template("taskreport.html", completed_todoitems = completed_todoitems)










