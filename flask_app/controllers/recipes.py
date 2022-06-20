from flask_app import app
from flask_bcrypt import Bcrypt
from flask import render_template,request,redirect,session,flash
from flask_app.models import user,recipe
from datetime import datetime
bcrypt = Bcrypt(app)

@app.route('/new/recipe')
def new_recipe():
        if 'user_id' not in session:
                return redirect ('/logout')
        data = {
                "id": session['user_id']
        }
        print(session['user_id'])
        return render_template('create_recipe.html',user=user.User.get_by_id(data))

@app.route('/recipe/create', methods=["POST"])
def create_recipe():
        if 'user_id' not in session:
                return redirect ('/logout')
        if not recipe.Recipe.validate_recipe(request.form):
                return redirect('/new/recipe')
        data ={
                "user_id": session['user_id'],
                "name" : request.form['name'],
                "description" : request.form['description'],
                "instruction" : request.form['instruction'],
                "under_30_min" : int(request.form['under_30_min']),
                "date_made": request.form['date_made']
        }
        recipe.Recipe.create(data)
        return redirect('/dashboard')

@app.route('/recipe/<int:id>')
def show_recipe(id):
        if 'user_id' not in session:
                return redirect ('/logout')
        recipe_data = {
                "id": id
        }
        user_data={
                "id": session['user_id']
        }
        display_recipe = recipe.Recipe.get_one(recipe_data)
        one_user = user.User.get_by_id(user_data)
        return render_template("recipes.html",display = display_recipe, user=one_user)

@app.route('/recipe/edit/<int:id>')
def edit_recipe(id):
        if 'user_id' not in session:
                return redirect ('/logout')
        recipe_data={
                "id":id
        }
        user_data={
                "id": session['user_id']
        }
        one_r= recipe.Recipe.get_one(recipe_data)
        one_u= user.User.get_by_id(user_data)
        return render_template ("update_recipe.html", one_r = one_r, one_u = one_u)

@app.route('/recipe/update/<int:id>', methods=["POST"])
def update_recipe(id):
        if 'user_id' not in session:
                return redirect ('/logout')
        if not recipe.Recipe.validate_recipe(request.form):
                return redirect (f"/recipe/update/{recipe.id}")        
        recipe_data = {
                "id":request.form['id'],
                "user_id": session['user_id'],
                "name" : request.form['name'],
                "description" : request.form['description'],
                "instruction" : request.form['instruction'],
                "under_30_min" : int(request.form['under_30_min']),
                "date_made": request.form['date_made'],
        }
        recipe.Recipe.update(recipe_data)
        return redirect ('/dashboard')

@app.route('/recipe/delete/<int:id>')
def delete_recipe(id):
        if 'user_id' not in session:
                return redirect ('/logout')
        data={
                "id": session['user_id']
        }
        recipe.Recipe.delete(data)
        return redirect ('/dashboard')