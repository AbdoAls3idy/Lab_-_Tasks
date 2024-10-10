#!/usr/bin/env python3

import json
import requests
import urllib3
from base64 import b64encode

# Disable insecure https warnings (for self-signed SSL certificates)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
protocol = 'https'
host = '18.197.23.142'
port = 55000
user = 'wazuh'
password = 'CGOU.jCG+9g8r7BZxMLDlv7VxMs2o*wA'
login_endpoint = 'security/user/authenticate'

login_url = f"{protocol}://{host}:{port}/{login_endpoint}"
basic_auth = f"{user}:{password}".encode()
login_headers = {'Content-Type': 'application/json',
                 'Authorization': f'Basic {b64encode(basic_auth).decode()}'}

print("\nLogin request ...\n")
response = requests.post(login_url, headers=login_headers, verify=False)
if response.status_code == 200:
    token = json.loads(response.content.decode())['data']['token']
    print(f"Login successful. Token: {token}")
else:
    print(f"Login failed: {response.status_code}")
    exit(1)

# authorization header with the JWT token
requests_headers = {'Content-Type': 'application/json',
                    'Authorization': f'Bearer {token}'}

def get_agents_status():
    print("\nGetting agents status summary:")
    response = requests.get(f"{protocol}://{host}:{port}/agents/summary/status?pretty=true", headers=requests_headers, verify=False)
    if response.status_code == 200:
        print(response.text)
    else:
        print(f"Error retrieving agents summary: {response.status_code}")


        print(f"Failed to retrieve the Threat Hunting Report: {response.status_code}")

if __name__ == '__main__':
    print("\n- API calls with TOKEN environment variable ...\n")

    print("Getting API information:")
    response = requests.get(f"{protocol}://{host}:{port}/?pretty=true", headers=requests_headers, verify=False)
    if response.status_code == 200:
        print(response.text)
    else:
        print(f"Error retrieving API information: {response.status_code}")
    
    # Get agent status
    get_agents_status()

    print("\nEnd of the script.\n")
