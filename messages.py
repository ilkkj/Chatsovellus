from db import db
from sqlalchemy.sql import text
import users

def get_list():
    sql = """
    SELECT M.content, U.username, M.sent_at 
    FROM messages M, users U 
    WHERE M.user_id=U.user_id 
    ORDER BY M.message_id
    """
    result = db.session.execute(text(sql))
    return result.fetchall()

def get_categories():
    sql = "SELECT C.name FROM categories C ORDER BY C.name"
    result = db.session.execute(text(sql))
    return result.fetchall()

def get_threads():
    sql = "SELECT name, thread_id FROM threads ORDER BY thread_id"
    result = db.session.execute(text(sql))
    return result.fetchall()

def check_categories(name):
    sql = "SELECT name, category_id FROM categories WHERE name = :name;"
    result = db.session.execute(text(sql), {"name": name})
    return result.fetchone()

def check_threads(id):
    sql = "SELECT thread_id, name FROM threads WHERE thread_id = :id;"
    result = db.session.execute(text(sql), {"id": id})
    return result.fetchone()

def get_list_for_thread(thread_id):
    sql = """
    SELECT M.content, U.username, M.sent_at 
    FROM messages M, users U 
    WHERE M.user_id=U.user_id AND M.thread_id=:thread_id 
    ORDER BY M.message_id
    """
    result = db.session.execute(text(sql), {"thread_id": thread_id})
    return result.fetchall()

def get_list_for_category(category_id):
    sql = """
    SELECT T.thread_id, T.name, U.username
    FROM threads T
    JOIN users U ON T.user_id = U.user_id
    WHERE T.category_id = :category_id
    ORDER BY T.thread_id
    """
    result = db.session.execute(text(sql), {"category_id": category_id})
    return result.fetchall()

def send(content, category_id, thread_id):
    if category_id is None or thread_id is None:
        return False
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = """
    INSERT INTO messages (content, user_id, thread_id, category_id, sent_at) 
    VALUES (:content, :user_id, :thread_id, :category_id, NOW())
    """
    db.session.execute(text(sql), {"content":content, "user_id":user_id, "thread_id":thread_id, "category_id":category_id})
    db.session.commit()
    return True