from sys import argv
from requests import post
import json
if len(argv) != 4:
    raise Exception("Provide Proper Inputs")
URL = argv[1]
projectName = argv[2]
deployMethod = argv[3]

data = {
    'projectName': projectName,
    'deployMethod': deployMethod
}
headers = {
    "Content-Type": "application/json"
}
response = post(URL,data=json.dumps(data),headers=headers)
if response.status_code != 200:
    raise Exception(response.json())