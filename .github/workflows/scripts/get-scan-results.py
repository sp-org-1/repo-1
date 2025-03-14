import requests
import os
import sys
import json
import uuid
import boto3
from requests.auth import HTTPBasicAuth

def add_comment_to_commit(token, comment):
    url = f"https://api.github.com/repos/sp-org-1/repo-1/commits/b5c2d45afde9a3327dc44cb7b81ddd81b3c0e016/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    data = {"body": comment}
    print(comment)
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response)

def invoke_agent(promptfiles):
    client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
    
    # Generate unique session ID
    session_id = uuid.uuid4().hex
    print("session_id:", session_id)

    # Generate prompt
    finaloutput = "### Suggestions by AI-Assist for vulnerabilities found by SonarQube scan\n"
    for file in promptfiles:
        with open(file, 'r') as file:
            content = file.read()
            #print("Following is the prompt to agent:")
            #print("===========================================")
            #print(content)
            #print("===========================================")
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
            finaloutput = finaloutput + completion + "\n"
            
    return finaloutput
    #print(finaloutput)
    #print("===========================================")
    # Add comment to git commit
    #add_comment_to_commit(token, finaloutput)

            
    #with open('prompt.txt', 'r') as file:
    #    content = file.read()
    #print(promptfiles)
    # Invoke agent
    
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
    #print(response.text)
    # Parse the JSON response
    jsonout = json.loads(response.text)
    issues = jsonout.get('issues', [])
    promptfiles = []
    for issue in issues:
        if issue.get('status') == "CLOSED":
            continue
            
        # Get filename having vulnerabilities
        filename = issue.get('component').split(":")[1]

        # Check if it is first issue, then add the prompt and source file contents
        promptfilename = filename + ".prompt"
        if os.path.exists(promptfilename):
            ## File exists, subsequent entry
            f = open(promptfilename, "a")
        else:
            ## File does not exists, first entry
            promptfiles.append(promptfilename)
            f = open(promptfilename, "a")
            # Add prompt
            with open(".github/workflows/scripts/action-prompt.txt", 'r') as file:
                content = file.read()
                f.write(content + "\n")
            # Add source code
            f.write("Source Code:" + "\n")
            f.write("Filename: " + filename + "\n")
            f.write("```\n")
            with open(filename, 'r') as file:
                content = file.read()
                f.write(content + "\n")
            f.write("```\n")
            f.write("Vulnerability Details:\n")    
            
        # Get vulnerability details
        key = issue.get('key')
        f.write("key:" + key + "\n")
        rule = issue.get('rule')
        f.write("rule:" + rule + "\n")
        message = issue.get('message')
        f.write("message:" + message + "\n")
        if(issue.get('textRange') != None):
            startline = issue.get('textRange').get('startLine')
            f.write("startline:" + str(startline) + "\n")
            endline = issue.get('textRange').get('endLine')  
            f.write("endline:" + str(endline) + "\n")
            startoffset = issue.get('textRange').get('startOffset')
            f.write("startoffset:" + str(startoffset) + "\n")
            endoffset = issue.get('textRange').get('endOffset')  
            f.write("endoffset:" + str(endoffset) + "\n")
        f.write("------\n")
        f.close()

    return promptfiles
    
# Execution starts here
promptfiles = get_scan_results(sys.argv[1])
finaloutput = invoke_agent(promptfiles)
add_comment_to_commit(sys.argv[2], finaloutput)
