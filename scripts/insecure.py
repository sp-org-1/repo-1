import sqlite3
import json
import requests
import sys
from requests.auth import HTTPBasicAuth

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
#print(user_data)

username = sys.argv[1]
password = ""
headers = {
    'Accept': 'application/json',
}
params = {
    'organization': 'sp-org-1',
    'projects': 'sp-org-1_repo-1',
}
response = requests.get('https://sonarcloud.io/api/issues/search', params=params, headers=headers, auth=HTTPBasicAuth(username, password))
#print(response)
#print(response.text)


# Parse the JSON response
jsonout = json.loads(response.text)
#print(jsonout)

# Test comment
# Test comment1
