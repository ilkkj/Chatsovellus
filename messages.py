from db import db
from sqlalchemy.sql import text
import users
import re

def get_categories():
    sql = """
    WITH user_rights AS (
        SELECT 
            r.user_id, 
            r.is_admin, 
            r.secret_areas
        FROM rights r
        WHERE r.user_id = :user_id
    )
    SELECT 
        c.name AS category_name,
        c.category_id AS category_id, 
        COUNT(DISTINCT t.thread_id) AS thread_count,
        COUNT(m.message_id) AS message_count,
        SUM(COUNT(m.message_id)) OVER() AS message_sum,
        TO_CHAR(MAX(m.sent_at), 'DD/MM/YYYY HH24:MI') AS last_message_time 
    FROM 
        categories c
    LEFT JOIN 
        threads t ON c.category_id = t.category_id
    LEFT JOIN 
        messages m ON t.thread_id = m.thread_id
    LEFT JOIN 
        user_rights ur ON TRUE
    WHERE 
        c.is_secret = FALSE
        OR ur.is_admin = TRUE
        OR c.category_id = ANY(ur.secret_areas)
    GROUP BY 
        c.category_id 
    ORDER BY 
        c.name
    """
    result = db.session.execute(text(sql), {'user_id': users.user_id()})
    return result.fetchall()



def get_threads(category_id):
    sql = """
    SELECT 
        t.name AS thread_name,
        t.thread_id,
        t.user_id,
        COUNT(m.message_id) AS message_count,
        TO_CHAR(MAX(m.sent_at), 'DD/MM/YYYY HH24:MI') AS last_message_time 
    FROM 
        threads t
    LEFT JOIN 
        messages m ON t.thread_id = m.thread_id
    WHERE
        t.category_id = :category_id
    GROUP BY 
        t.thread_id
    """
    result = db.session.execute(text(sql), {"category_id": category_id})
    return result.fetchall()



def get_messages(thread_id):
    sql = """
    SELECT 
        m.message_id, 
        m.content, 
        u.username,
        m.user_id, 
        TO_CHAR(m.sent_at,'DD/MM/YYYY HH24:MI') AS sent_at 
    FROM 
        messages m 
    LEFT JOIN 
        users u ON m.user_id = u.user_id 
    WHERE 
        thread_id = :thread_id 
    ORDER BY 
        m.message_id
    """
    result = db.session.execute(text(sql), {"thread_id": thread_id})
    return result.fetchall()



def check_categories(name):
    sql = """
    SELECT 
        name, 
        category_id 
    FROM 
        categories 
    WHERE 
        name = :name;
    """
    result = db.session.execute(text(sql), {"name": name})
    return result.fetchone()



def check_threads(thread_id, category_id):
    sql = """
    SELECT 
        name, 
        thread_id 
    FROM 
        threads 
    WHERE 
        thread_id = :thread_id
        AND category_id = :category_id;
    """
    result = db.session.execute(text(sql), {"thread_id": thread_id, "category_id": category_id})
    return result.fetchone()



def create_category(category_name, is_secret):
    if not users.check_admin():
        return False
    sql = """
    INSERT INTO 
        categories (name, is_secret)
    VALUES 
        (:name, :is_secret)
    """
    db.session.execute(text(sql), {"name":category_name, "is_secret":is_secret})
    db.session.commit()
    return True



def delete_category(category_id):
    if not users.check_admin():
        return False
    sql = """
    DELETE FROM 
        categories 
    WHERE 
        category_id = :category_id
    """
    db.session.execute(text(sql), {"category_id":category_id})
    db.session.commit()
    return True



def create_thread(category_id, thread_name):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = """
    INSERT INTO 
        threads (user_id, name, category_id)
    VALUES 
        (:user_id, :name, :category_id)
    RETURNING 
        thread_id
    """
    thread_id = db.session.execute(text(sql), {"user_id":user_id, "name":thread_name, "category_id":category_id}).first()[0]
    return thread_id



def edit_thread(thread_name, thread_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    if not re.search(r"\S", thread_name):
        return False
    sql = """
    UPDATE 
        threads 
    SET 
        name = :thread_name
    WHERE 
        thread_id = :thread_id AND user_id = :user_id
    """
    db.session.execute(text(sql), {"thread_name":thread_name, "thread_id":thread_id, "user_id":user_id})
    db.session.commit()
    return True



def delete_thread(thread_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = """
    DELETE FROM 
        threads 
    WHERE 
        thread_id = :thread_id AND user_id = :user_id
    """
    db.session.execute(text(sql), {"thread_id":thread_id, "user_id":user_id})
    db.session.commit()
    return True



def send_message(content, category_id, thread_id):
    if category_id is None or thread_id is None:
        return False
    user_id = users.user_id()
    if user_id == 0:
        return False
    if not re.search(r"\S", content):
        return False
    sql = """
    INSERT INTO 
        messages (content, user_id, thread_id, category_id) 
    VALUES 
        (:content, :user_id, :thread_id, :category_id)
    """
    db.session.execute(text(sql), {"content":content, "user_id":user_id, "thread_id":thread_id, "category_id":category_id})
    db.session.commit()
    return True



def edit_message(content, message_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    if not re.search(r"\S", content):
        return False
    sql = """
    UPDATE 
        messages 
    SET 
        content = :content,
        edited_at = NOW() 
    WHERE 
        message_id = :message_id AND user_id = :user_id
    """
    db.session.execute(text(sql), {"content":content, "message_id":message_id, "user_id":user_id})
    db.session.commit()
    return True



def delete_message(message_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = """
    DELETE FROM 
        messages 
    WHERE 
        message_id = :message_id AND user_id = :user_id
    """
    db.session.execute(text(sql), {"message_id":message_id, "user_id":user_id})
    db.session.commit()
    return True