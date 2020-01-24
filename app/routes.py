from app import app

# Home Page URL Route
@app.route('/')
@app.route("/index")
def index():
    return "Task Management System"