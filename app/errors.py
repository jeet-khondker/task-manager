# Custom Error Handlers
from flask import render_template
from app import app, db

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server(error):
    db.session.rollback()
    return render_template("500.html"), 500