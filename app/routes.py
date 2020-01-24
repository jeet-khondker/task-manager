from flask import render_template
from app import app

# Home Page URL Route
@app.route('/')
@app.route("/index")
def index():
    return render_template("index.html")