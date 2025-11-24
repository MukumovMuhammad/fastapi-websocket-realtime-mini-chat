import sqlite3

connect = sqlite3.connect("DATA.db")

cursor = connect.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT,
    online_status TEXT
)
''')

def add_user(name, password):
    if is_user_exist(name):
        return {"message": "user already exists", "status": False}
    cursor.execute('''
           INSERT INTO users (username, password, online_status) VALUES (?,?,?)
       ''', (name,password,1))
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
    cursor.execute(f'SELECT username, id FROM users')
    users = cursor.fetchall()
    print("Users ", users)
    formated_usernames = []
    if users:
        for i in users:
            formated_usernames.append(i)
        return formated_usernames
    return []

def set_user_online_status(id: int, status: int):
    cursor.execute("UPDATE users SET online_status = ? WHERE id = ?", (status, id))
    connect.commit()

def get_users_online():
    cursor.execute("SELECT id FROM users WHERE online_status = 1")
    data = cursor.fetchall()
    # print(f"the fetched data {data}")
    formated_data = []
    for i in data:
        # print(f"the i in the loop {i}")
        formated_data.append(i[0])
    # print(f"the formated data! {formated_data}")
    return formated_data

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
    return False

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
    
