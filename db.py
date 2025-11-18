import sqlite3

connect = sqlite3.connect("DATA.db")

cursor = connect.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT
)
''')

def add_user(name, password):
    if is_user_exist(name):
        return {"message": "user already exists", "status": False}
    cursor.execute('''
           INSERT INTO users (username, password) VALUES (?,?)
       ''', (name,password))
    connect.commit()
    return {"message": "user added", "status": True, "id": get_user_id(name) }

def check_password(username, password):
    if not is_user_exist(username):
        return False

    
    cursor.execute(" SELECT COUNT(*) FROM users WHERE username = ? AND password = ?", (username, password))
    
    # Fetch the result (a single number: 1 if match found, 0 otherwise)
    count = cursor.fetchone()[0]
    
    return  count == 1
     

def get_usernames():
    cursor.execute(f'SELECT username FROM users')
    users = cursor.fetchall()
    print("Users ", users)
    formated_usernames = []
    if users:
        for i in users:
            formated_usernames.append(i)
        return formated_usernames
    return []

def get_user_id(username):
    query = f"SELECT id FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    user = cursor.fetchone()[0]
    print("get a user by id data is - > ", user)
    return user

def get_a_user_by(type, value):
    query = f"SELECT * FROM users WHERE {type} = ?"
    cursor.execute(query, (value,))
    user = cursor.fetchone()
    if user:
        return user
    return "NO data"

def delete_user(client_id):
    print(f"Got data {client_id}")
    cursor.execute("DELETE FROM users WHERE client_id = ?", (client_id,))
    connect.commit()

def is_user_exist(user):
    cursor = connect.cursor()
    query = f"SELECT EXISTS(SELECT 1 FROM users WHERE username = ?)"
    cursor.execute(query, (user,))

    # fetchone() returns a tuple; the existence value is the first element
    exists = cursor.fetchone()[0]
    return exists == 1
    
