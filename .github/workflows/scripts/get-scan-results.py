import requests
import sys
import json
from requests.auth import HTTPBasicAuth

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

# Parse the JSON response
jsonout = json.loads(response.text)
issues = jsonout.get('issues', [])
for issue in issues:
    if issue.get('status') == "CLOSED":
        continue
    f = open("prompt.txt", "a")
    with open("action-prompt.txt", 'r') as file:
        content = file.read()
        f.write(content + "\n")
    f.write("Vulnerability Details\n")
    f.write("```\n")
    key = issue.get('key')
    f.write("key:" + key + "\n")
    rule = issue.get('rule')
    f.write("rule:" + rule + "\n")
    message = issue.get('message')
    f.write("message:" + message + "\n")
    if(issue.get('textRange') == None):
        continue
    startline = issue.get('textRange').get('startLine')
    f.write("startline:" + str(startline) + "\n")
    endline = issue.get('textRange').get('endLine')  
    f.write("endline:" + str(endline) + "\n")
    startoffset = issue.get('textRange').get('startOffset')
    f.write("startoffset:" + str(startoffset) + "\n")
    endoffset = issue.get('textRange').get('endOffset')  
    f.write("endoffset:" + str(endoffset) + "\n")
    f.write("```\n")
    f.write("File Contents" + "\n")
    f.write("```\n")
    filename = issue.get('component').split(":")[1]
    with open(filename, 'r') as file:
        content = file.read()
        f.write(content + "\n")
    f.write("```\n")
    f.close()

    with open("prompt.txt", 'r') as file:
        content = file.read()
        print(content)
    
    break
