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
#print(response)
#print(response.text)


# Parse the JSON response
jsonout = json.loads(response.text)
#print(jsonout)
#print("====")
#print(json.dumps(jsonout))
issues = jsonout.get('issues', [])
for issue in issues:
    if issue.get('status') == "CLOSED":
        continue
    print("------")
    key = issue.get('key')
    print("key:", key)
    rule = issue.get('rule')
    print("rule:", rule)
    message = issue.get('message')
    print("message:", message)
    filename = issue.get('component').split(":")[1]
    print("filename:", filename)
    if(issue.get('textRange') == None):
        continue
    startline = issue.get('textRange').get('startLine')
    print("startline:", startline)
    endline = issue.get('textRange').get('endLine')  
    print("endline:", endline)
    startoffset = issue.get('textRange').get('startOffset')
    print("startoffset:", startoffset)
    endoffset = issue.get('textRange').get('endOffset')  
    print("endoffset:", endoffset)
    with open(filename, 'r') as file:
        content = file.read()
        print(content)
    #print(f"Issue Key: {issue.get('key')}")
    #print(f"Severity: {issue.get('severity')}")
    #print(f"Message: {issue.get('message')}")
    #print(f"Component: {issue.get('component')}")
    #print(f"Project: {issue.get('project')}")
    #print("------")
