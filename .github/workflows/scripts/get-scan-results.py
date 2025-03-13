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
    f.write("Vulnerability Details")
    f.write("```")
    key = issue.get('key')
    f.write("key:" + key)
    rule = issue.get('rule')
    f.write("rule:" + rule)
    message = issue.get('message')
    f.write("message:" + message)
    if(issue.get('textRange') == None):
        continue
    startline = issue.get('textRange').get('startLine')
    f.write("startline:" + startline)
    endline = issue.get('textRange').get('endLine')  
    f.write("endline:" + endline)
    startoffset = issue.get('textRange').get('startOffset')
    f.write("startoffset:" + startoffset)
    endoffset = issue.get('textRange').get('endOffset')  
    f.write("endoffset:" + endoffset)
    f.write("```")
    f.write("File Contents")
    f.write("```")
    filename = issue.get('component').split(":")[1]
    with open(filename, 'r') as file:
        content = file.read()
        f.write(content)
    f.write("```")
    f.close()

    with open(prompt.txt, 'r') as file:
        content = file.read()
        f.write(content)
    
    break
