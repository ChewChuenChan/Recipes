from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import recipe
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "recipes_schema"

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes =[]

    @classmethod
    def create(cls,data):
        query = """
        INSERT INTO users (first_name, last_name, email, password, created_at, updated_at )
        VALUES 
        (%(first_name)s, %(last_name)s, %(email)s, %(password)s , NOW() , NOW());
        """
        result = connectToMySQL(cls.db).query_db(query,data)
        print(result)
        return result

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        result = connectToMySQL(cls.db).query_db(query)
        users_list = []
        for row in result:
            users_list.append(cls(row))
        return users_list
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email =%(email)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        if len(result) < 1:
            return False
        this_user = cls(result[0])
        return this_user

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id =%(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        if len(result) < 1:
            return False
        this_user = cls(result[0])
        return this_user

    @staticmethod
    def validate_register( user ):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(User.db).query_db(query,user)
        if len(result) >=1:
            flash("Email already taken.","register")
            is_valid = False
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email","register") 
            is_valid = False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.","register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.","register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.","register")
            is_valid = False
        if not (user['password']) == (user['confirm_pass']):
            flash("Passwords don't match","register")
            is_valid = False
        return is_valid


    # @classmethod
    # def get_user_with_recipes(cls,data):
    #     query="""
    #     SELECT * FROM users 
    #     LEFT JOIN recipes 
    #     ON users.id = recipes.user_id 
    #     WHERE users.id =%(id)s;"""
    #     results = connectToMySQL(cls.db).query_db(query,data)
    #     print(results)
    #     user_with_recipes = cls (results[0])
    #     print(user_with_recipes)
    #     for row in results:
    #         recipe_data ={
    #             "id" : row['recipes.id'],
    #             "name" : row['name'],
    #             "description" : row['description'],
    #             "instruction" : row['instruction'],
    #             "under_30_min" : row['under_30_min'],
    #             "date_made": row['date_made'],
    #             "created_at" : row['recipes.created_at'],
    #             "updated_at" : row['recipes.updated_at'],
    #             "user_id":row['user_id']
    #         }
    #         user_with_recipes.recipes.append (recipe.Recipe( recipe_data))
    #     return user_with_recipes


