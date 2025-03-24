import requests
import sys
import json
from requests.auth import HTTPBasicAuth

def get_language_loc(sonar_token, project_name):
    # Set Sonarqibe creds
    username = sonar_token
    password = ""
    # Set headers and params
    headers = {
        'Accept': 'application/json',
    }
    params = {
        'component': project_name,
        'metricKeys': 'ncloc',
    }
    # Make a GET request to Sonarqube API
    response = requests.get('https://sonarcloud.io/api/measures/component_tree', params=params, headers=headers, auth=HTTPBasicAuth(username, password))
    
    # Supported languages
    languages = ["py", "java", "yaml", "xml"]
    #languages = ["py"]
    lang_loc_list = []
    
    # Parse the JSON response
    jsonout = json.loads(response.text)
    components = jsonout.get('components', [])
    for component in components:
        # Skip directory type components
        if component.get('qualifier') == "DIR":
            continue
        # Skip components with no measures, the file failed to scan
        if len(component.get('measures')) == 0:
            continue
        # Get the loc for the component and add it up to the map
        for language in languages:
            if component.get('language') == language:
                file_name = component.get('path')
                if(len(lang_loc_list))  == 0:
                    # This is the first entry in list
                    lang_loc_list.append({'lang':language, 'loc': str(component.get('measures')[0].get('value')), 'files': [file_name]})
                    break
                else:
                    # Existing entries available, see if the language is already present
                    for entry in lang_loc_list:
                        if entry['lang'] == language:
                            # Language already present, update it
                            entry['loc'] = str(int(entry['loc']) + int(component.get('measures')[0].get('value')))
                            entry['files'].append(file_name)
                            break
                        else:
                            # Language not present, append it
                            lang_loc_list.append({'lang':language, 'loc': str(component.get('measures')[0].get('value')), 'files': [file_name]})
                            break
    print("Project: " + project_name)                
    print(json.dumps(lang_loc_list))

# Execution starts here
get_language_loc(sys.argv[1], sys.argv[2])
