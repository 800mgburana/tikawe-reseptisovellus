import db
from flask import redirect

def get_recipes():
    sql = """SELECT r.id, r.title, r.date, r.status, u.username, r.user_id
             FROM recipes r, users u
             WHERE r.user_id = u.id
             ORDER BY r.id DESC"""
    
    return db.query(sql)

def get_recipe(recipe_id):
    sql = """SELECT r.id, r.title, r.ingredients, r.instructions, 
             r.date, r.status, u.username, r.user_id
             FROM recipes r, users u 
             WHERE r.id = ? AND r.user_id = u.id"""
    
    return db.query(sql, [recipe_id])[0]

def update_recipe(recipe_id, title, ingredients, instructions):
    sql = """UPDATE recipes
             SET title = ?,
                 ingredients = ?,
                 instructions = ?
             WHERE id = ?;"""
    
    db.execute(sql, [title, ingredients, instructions, recipe_id])

def delete_recipe(recipe_id):
    sql = """UPDATE recipes
             SET status = 0
             WHERE id = ?"""
    
    db.execute(sql, [recipe_id])

def search(query):
    sql = """SELECT r.id recipe_id, r.title, r.ingredients,
                    r.date, u.username
             FROM recipes r, users u
             WHERE r.user_id = u.id AND r.title LIKE ?
             ORDER BY r.date DESC"""
    
    return db.query(sql, ["%" + query + "%"])