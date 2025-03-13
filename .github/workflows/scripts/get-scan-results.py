import requests
import sys
from requests.auth import HTTPBasicAuth

username = sys.argv[0]
password = ""
headers = {
    'Accept': 'application/json',
}
params = {
    'organization': 'sp-org-1',
    'projects': 'sp-org-1_repo-1',
}
response = requests.get('https://sonarcloud.io/api/issues/search', params=params, headers=headers, auth=HTTPBasicAuth(username, password))
print(response)
#print(response.json())
