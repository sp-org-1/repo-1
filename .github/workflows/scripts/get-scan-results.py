import requests
import sys
import json
import uuid
import boto3
from requests.auth import HTTPBasicAuth

def invoke_agent():
    client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
    
    # Generate unique session ID
    session_id = uuid.uuid4().hex
    print("session_id:", session_id)

    # Generate prompt
    with open('prompt.txt', 'r') as file:
        content = file.read()

    # Invoke agent
    response = client.invoke_agent(
        agentId='CM3GUGONHG',
        agentAliasId='HIEAMVWWIC',
        sessionId=session_id,
        inputText=content,
    )
    completion = ""
    
    # Extract completion from response
    for event in response.get("completion"):
        chunk = event["chunk"]
        completion += chunk["bytes"].decode()
    print("Following is the response from agent:")
    print("===========================================")
    print(completion)
    print("===========================================")

def get_scan_results(sonar_token):
    username = sonar_token
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
        # Get vulnerability details
        filename = issue.get('component').split(":")[1]
        key = issue.get('key')
        rule = issue.get('rule')
        message = issue.get('message')
        startline = issue.get('textRange').get('startLine')
        endline = issue.get('textRange').get('endLine')  
        startoffset = issue.get('textRange').get('startOffset')
        endoffset = issue.get('textRange').get('endOffset')  

        promptfilename = filename + ".prompt"
        if os.path.exists(promptfilename):
            ## File exists, subsequent entry
            f = open(promptfilename, "a")
        else:
            ## File does not exists, first entry
            f = open(promptfilename, "a")
            # Add prompt
            with open(".github/workflows/scripts/action-prompt.txt", 'r') as file:
                content = file.read()
                f.write(content + "\n")
            # Add source code
            f.write("Source Code:" + "\n")
            f.write("```\n")
            with open(filename, 'r') as file:
                content = file.read()
                f.write(content + "\n")
            f.write("```\n")
            f.write("Vulnerability Details:\n")    
        
        f.write("key:" + key + "\n")
        f.write("rule:" + rule + "\n")
        f.write("message:" + message + "\n")
        if(issue.get('textRange') == None):
            continue
        f.write("startline:" + str(startline) + "\n")
        f.write("endline:" + str(endline) + "\n")
        f.write("startoffset:" + str(startoffset) + "\n")
        f.write("endoffset:" + str(endoffset) + "\n")
        f.write("------\n")
        f.close()
    
        #with open(promptfilename, 'r') as file:
        #    content = file.read()
        #    print(content)
    
    current_directory = os.getcwd()    
    files = os.listdir(current_directory)
    for file in files:
        print(file)
    
# Execution starts here
get_scan_results(sys.argv[1])
#invoke_agent()
