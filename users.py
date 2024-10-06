from db import db
from sqlalchemy.sql import text
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = """
    SELECT 
        u.user_id, 
        u.password 
    FROM 
        users u 
    WHERE 
        u.username = :username
    """
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.user_id
            return True
        else:
            return False

def logout():
    del session["user_id"]

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        db.session.execute(text(sql), {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id",0)

def check_rights(category_id):
    sql = """
    SELECT 
        CASE 
            WHEN r.is_admin THEN TRUE
            WHEN c.is_secret AND :category_id = ANY(r.secret_areas) THEN TRUE
            WHEN c.is_secret IS FALSE THEN TRUE
            ELSE FALSE
        END AS has_access
    FROM 
        rights r
    JOIN 
        categories c ON c.category_id = :category_id
    WHERE 
        r.user_id = :user_id OR :user_id = 0
    """
    result = db.session.execute(text(sql), {'user_id': user_id(), 'category_id': category_id})
    return result.fetchone()[0]

def check_admin():
    if user_id() == 0 or not user_id():
        return False
    sql = """
    SELECT 
        CASE 
            WHEN r.is_admin THEN TRUE 
            ELSE FALSE 
        END AS is_admin 
    FROM 
        rights r 
    WHERE 
        r.user_id = :user_id OR :user_id = 0
    """
    result = db.session.execute(text(sql), {'user_id': user_id()})
    if result == None:
        return False
    return result.fetchone()[0]