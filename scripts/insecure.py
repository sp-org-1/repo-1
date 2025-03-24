import sqlite3

def get_user(username):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    result = cursor.fetchone()
    connection.close()
    return result

username_input = input("Enter username: ")
user_data = get_user(username_input)
print(user_data)

# Test comment
# Test comment1
