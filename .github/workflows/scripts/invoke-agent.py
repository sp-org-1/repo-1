import uuid
import boto3
import sys
             
# Read arguments
action_prompt_file = sys.argv[1]

client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

# Generate unique session ID
session_id = uuid.uuid4().hex
print("session_id:", session_id)

# Generate prompt from git diff and action prompt
prompt = ""
with open('git-diff.txt', 'r') as file:
    content = file.read()
prompt = prompt + content
with open(action_prompt_file, 'r') as file:
    content = file.read()
prompt = prompt + content
print("Following prompt will be sent to the agent:")
print("===========================================")
print(prompt)
print("===========================================")

# Invoke agent
response = client.invoke_agent(
    agentId='KRQF44CTQU',
    agentAliasId='JM7CRIDG7D',
    sessionId=session_id,
    inputText=prompt,
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

# Write response to file
f = open("agent-response.txt", "w")
f.write(completion)
f.close()
