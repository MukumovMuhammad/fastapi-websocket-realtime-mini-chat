import sqlite3

connect = sqlite3.connect("DATA.db")

cursor = connect.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    client_id INT
)
''')

def add_user(name, id):
    cursor.execute('''
           INSERT INTO users (username, client_id) VALUES (?,?)
       ''', (name,id))
    connect.commit()

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
