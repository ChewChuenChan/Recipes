from flask_app import app
from flask_bcrypt import Bcrypt
from flask import render_template,request,redirect,session,flash
from flask_app.models import user,recipe
from datetime import datetime
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=["POST"])
def register():
    if not user.User.validate_register(request.form):
        return redirect('/')
    data ={
        "first_name" :request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : bcrypt.generate_password_hash(request.form["password"])
        }
    user_id = user.User.create(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/login',methods =['POST'])
def login():
    this_user = user.User.get_by_email({"email" : request.form["email"]})
    if this_user and bcrypt.check_password_hash(this_user.password,request.form['password']):
        session['user_id'] = this_user.id
        return redirect('/dashboard') 
    flash("Invalid Email/Password","login")
    return redirect ('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect ('/logout')
    data = {
        'id': session['user_id']
    }
    print(type(session['user_id']),session ['user_id'])
    this_user = user.User.get_by_id(data)
    recipes = recipe.Recipe.get_all()
    return render_template("dashboard.html", this_user=this_user, recipes=recipes)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')