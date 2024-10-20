from db import db
from sqlalchemy.sql import text
import users
import re

def get_categories():
    sql = """
    WITH user_rights AS (
        SELECT 
            r.user_id, 
            r.is_admin 
        FROM rights r 
        WHERE r.user_id = :user_id
    )
    SELECT 
        c.name AS category_name,
        c.category_id AS category_id, 
        c.is_secret AS is_secret,
        c.allowed_users,
        COUNT(DISTINCT t.thread_id) AS thread_count,
        COUNT(m.message_id) AS message_count,
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
        OR :user_id = ANY(c.allowed_users)
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
        t.content AS thread_content,
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
    ORDER BY 
        t.thread_id DESC
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
        TO_CHAR(m.sent_at,'DD/MM/YYYY HH24:MI') AS sent_at,
        TO_CHAR(m.edited_at,'DD/MM/YYYY HH24:MI') AS edited_at 
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
        category_id, 
        is_secret 
    FROM 
        categories 
    WHERE 
        name = :name
    """
    result = db.session.execute(text(sql), {"name": name})
    return result.fetchone()



def check_categories_unique(name, id):
    sql = """
    SELECT 
        name, 
        category_id, 
        is_secret 
    FROM 
        categories 
    WHERE 
        name = :name 
        AND category_id != :id
    """
    result = db.session.execute(text(sql), {"name": name, "id": id})
    return result.fetchone()



def check_threads(thread_id, category_id):
    sql = """
    SELECT 
        t.name,
        t.content,
        u.username, 
        t.thread_id,
        TO_CHAR(t.created_at,'DD/MM/YYYY HH24:MI') AS created_at,
        TO_CHAR(t.edited_at,'DD/MM/YYYY HH24:MI') AS edited_at 
    FROM 
        threads t 
    JOIN 
        users u ON u.user_id = t.user_id 
    WHERE 
        thread_id = :thread_id
        AND category_id = :category_id
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



def edit_category(category_id, category_name, is_secret, allowed_users):
    if not users.check_admin():
        return False
    sql = """
    UPDATE 
        categories 
    SET 
        name = :category_name,
        is_secret = :is_secret,
        allowed_users = :allowed_users
    WHERE 
        category_id = :category_id
    """
    db.session.execute(text(sql), {"category_name":category_name, "category_id":category_id,
                                    "is_secret":is_secret, "allowed_users":allowed_users})
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



def create_thread(content, category_id, thread_name):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = """
    INSERT INTO 
        threads (user_id, name, category_id, content)
    VALUES 
        (:user_id, :name, :category_id, :content)
    RETURNING 
        thread_id
    """
    thread_id = db.session.execute(text(sql), {"user_id":user_id, "name":thread_name,
                                                "category_id":category_id, "content":content}).first()[0]
    db.session.commit()
    return thread_id



def edit_thread(content, thread_name, thread_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = """
    UPDATE 
        threads 
    SET 
        name = :thread_name,
        content = :content,
        edited_at = NOW() 
    WHERE 
        thread_id = :thread_id AND user_id = :user_id
    """
    db.session.execute(text(sql), {"thread_name":thread_name, "content":content, 
                                   "thread_id":thread_id, "user_id":user_id})
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
    if not users.user_id():
        return False
    user_id = users.user_id()
    if not check_message(content):
        return False
    sql = """
    INSERT INTO 
        messages (content, user_id, thread_id, category_id) 
    VALUES 
        (:content, :user_id, :thread_id, :category_id)
    """
    db.session.execute(text(sql), {"content":content, "user_id":user_id, 
                                   "thread_id":thread_id, "category_id":category_id})
    db.session.commit()
    return True



def edit_message(content, message_id):
    if not users.user_id():
        return False
    user_id = users.user_id()
    if not check_message(content):
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



def check_category_title(title):
    if 1 <= len(title) <= 50:
        return bool(re.search(r'(?=\S)(?!.*\/)', title))



def check_thread_title(content):
    if 1 <= len(content) <= 100:
        return bool(re.search(r"\S", content))



def check_message(content):
    if 1 <= len(content) <= 20000:
        return bool(re.search(r"\S", content))
   



def search_categories(query):
    sql = """
    WITH user_rights AS (
        SELECT 
            r.user_id, 
            r.is_admin 
        FROM rights r 
        WHERE r.user_id = :user_id
    )
    SELECT 
        c.category_id,
        c.name AS category_name,
        COUNT(DISTINCT t.thread_id) AS thread_count,
        COUNT(m.message_id) AS message_count,
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
        c.name ILIKE '%' || :query || '%' 
        AND (
        c.is_secret = FALSE
        OR ur.is_admin = TRUE
        OR :user_id = ANY(c.allowed_users)
        )
    GROUP BY 
        c.category_id 
    ORDER BY 
        c.name
    """
    result = db.session.execute(text(sql), {"query": query, "user_id":users.user_id()})
    return result.fetchall()



def search_threads(query):
    sql = """
    WITH user_rights AS (
    SELECT 
        r.user_id, 
        r.is_admin 
    FROM rights r 
    WHERE r.user_id = :user_id
    )
    SELECT 
        t.thread_id,
        t.category_id,
        t.user_id,
        u.username,
        t.content,
        t.name AS thread_name,
        c.name AS category_name,
        COUNT(m.message_id) AS message_count,
        TO_CHAR(MAX(m.sent_at), 'DD/MM/YYYY HH24:MI') AS last_message_time 
    FROM 
        threads t
    JOIN 
        messages m ON m.thread_id = t.thread_id
    JOIN 
        categories c ON t.category_id = c.category_id 
    JOIN 
        users u ON t.user_id = u.user_id 
    LEFT JOIN 
        user_rights ur ON TRUE 
    WHERE (
        t.name ILIKE '%' || :query || '%' 
        OR t.content ILIKE '%' || :query || '%'
        ) 
        AND (
        c.is_secret = FALSE 
        OR ur.is_admin = TRUE
        OR :user_id = ANY(c.allowed_users)
        ) 
    GROUP BY 
        t.thread_id, 
        t.category_id, 
        t.user_id, 
        u.username, 
        t.content, 
        t.name, 
        c.name
    """
    result = db.session.execute(text(sql), {"query": query, "user_id":users.user_id()})
    return result.fetchall()



def search_messages(query):
    sql = """
    WITH user_rights AS (
        SELECT 
            r.user_id, 
            r.is_admin 
        FROM rights r 
        WHERE r.user_id = :user_id
    )
    SELECT 
        m.message_id,
        m.thread_id,
        m.category_id,
        m.user_id,
        u.username,
        m.content,
        TO_CHAR(m.sent_at,'DD/MM/YYYY HH24:MI') AS sent_at,
        TO_CHAR(m.edited_at,'DD/MM/YYYY HH24:MI') AS edited_at,
        c.name AS category_name,
        t.name AS thread_name
    FROM 
        messages m
    JOIN 
        categories c ON m.category_id = c.category_id
    JOIN 
        threads t ON m.thread_id = t.thread_id 
    JOIN 
        users u ON m.user_id = u.user_id 
    LEFT JOIN 
        user_rights ur ON TRUE 
    WHERE 
        m.content ILIKE '%' || :query || '%' 
        AND (
        c.is_secret = FALSE
        OR ur.is_admin = TRUE
        OR :user_id = ANY(c.allowed_users)
        )
    """
    result = db.session.execute(text(sql), {"query": query, "user_id":users.user_id()})
    return result.fetchall()