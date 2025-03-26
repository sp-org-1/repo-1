import requests
import sys
import json
from requests.auth import HTTPBasicAuth

def get_language_loc(sonar_token, project_name, api_url="https://sonarcloud.io/api/measures/component_tree"):
    """
    Fetches the language-wise LOC (Lines of Code) for a given project from SonarQube.
    """
    # Set SonarQube credentials
    username = sonar_token
    password = ""

    # Set headers and params
    headers = {'Accept': 'application/json'}
    params = {'component': project_name, 'metricKeys': 'ncloc'}

    try:
        # Make a GET request to SonarQube API
        response = requests.get(api_url, params=params, headers=headers, auth=HTTPBasicAuth(username, password))
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to fetch data from SonarQube API - {e}")
        sys.exit(1)

    # Parse the JSON response
    try:
        jsonout = response.json()
        print(json.dumps(jsonout))
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON response from SonarQube API")
        sys.exit(1)

    # Process components
    lang_loc_map = {'project': project_name, 'ncloc': []}
    lang_loc_dict = {}

    for component in jsonout.get('components', []):
        if component.get('qualifier') == "DIR":
            continue  # Skip directory components

        measures = component.get('measures', [])
        if not measures:
            continue  # Skip components with no measures

        language = component.get('language', 'unknown')
        loc = int(measures[0].get('value', 0))
        file_name = component.get('path', 'unknown')

        if language not in lang_loc_dict:
            lang_loc_dict[language] = {'loc': 0, 'files': []}

        lang_loc_dict[language]['loc'] += loc
        lang_loc_dict[language]['files'].append(file_name)

    # Convert dictionary to list format
    for lang, data in lang_loc_dict.items():
        lang_loc_map['ncloc'].append({'lang': lang, 'loc': str(data['loc']), 'files': data['files']})

    return lang_loc_map

# Execution starts here
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python sonarqube-get-lang-loc-for-project.py <sonar_token> <project_name>")
        sys.exit(1)

    sonar_token = sys.argv[1]
    project_name = sys.argv[2]
    result = get_language_loc(sonar_token, project_name)
    print(json.dumps(result, indent=4))