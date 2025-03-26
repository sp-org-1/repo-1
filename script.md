# Documentation: `sonarqube-get-lang-loc-for-project.py`

## Overview
This Python script retrieves the language-wise Lines of Code (LOC) for a specified project from SonarQube or SonarCloud. It uses the SonarQube API to fetch project metrics and organizes the LOC data by programming language.

---

## Prerequisites
- Python 3.x installed on your system.
- Access to a SonarQube or SonarCloud instance.
- A valid SonarQube API token.

---

## Usage
Run the script from the command line with the following syntax:

```bash
python sonarqube-get-lang-loc-for-project.py <sonar_token> <project_name>
```

### Parameters:
- `<sonar_token>`: Your SonarQube API token for authentication.
- `<project_name>`: The name of the project in SonarQube for which you want to fetch LOC data.

### Example:
```bash
python sonarqube-get-lang-loc-for-project.py my-sonar-token my-project-name
```

---

#### Example Output:
```json
{
    "project": "my-project-name",
    "ncloc": [
        {
            "lang": "Python",
            "loc": "1200",
            "files": ["file1.py", "file2.py"]
        },
        {
            "lang": "JavaScript",
            "loc": "800",
            "files": ["file1.js", "file2.js"]
        }
    ]
}
```

---

## Notes
- Ensure that the `sonar_token` has sufficient permissions to access the project metrics.
- The script assumes that the SonarQube API response contains the `components` and `measures` fields.

---

## License
This script is provided as-is without any warranty. Use it at your own risk.