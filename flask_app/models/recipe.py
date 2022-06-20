from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    db = "recipes_schema"

    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.under_30_min = data['under_30_min']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data ['user_id']

    @classmethod
    def create(cls,data):
        query = """
        INSERT INTO recipes 
        (name, description, instruction, under_30_min, date_made, user_id, created_at, updated_at ) 
        VALUES 
        (%(name)s, %(description)s, %(instruction)s, %(under_30_min)s, %(date_made)s, %(user_id)s, NOW() , NOW());"""
        result = connectToMySQL(cls.db).query_db(query,data)
        print(result)
        return result

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        result = connectToMySQL(cls.db).query_db(query)
        recipes_list = []
        for row in result:
            recipes_list.append(cls(row))
        return recipes_list

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        this_recipe = cls(result[0])
        print(this_recipe)
        return this_recipe

    @classmethod
    def update(cls,data):
        query = """
        UPDATE recipes SET 
        name = %(name)s, description = %(description)s, instruction =%(instruction)s, 
        under_30_min = %(under_30_min)s, date_made = %(date_made)s, user_id = %(user_id)s, 
        updated_at=Now() 
        WHERE id = %(id)s;  
        """
        print(query)
        result = connectToMySQL(cls.db).query_db(query,data)
        print(result)
        return result

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM recipes WHERE id =%(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validate_recipe( recipe ):
        is_valid = True
        if len(recipe['name']) < 3:
            flash("Name must be at least 3 characters ","recipe")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Description must be at least 3 characters","recipe")
            is_valid = False
        if len(recipe['instruction']) < 3:
            flash("Instruction must be at least 3 characters","recipe")
            is_valid = False
        if recipe['date_made'] == "":
            flash("Date must be select.","recipe")
            is_valid = False
        return is_valid