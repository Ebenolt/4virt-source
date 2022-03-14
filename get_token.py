# Usage: python3 script.py username@domain password
# Get API Token and call PS to setup user folder / network
import requests
import json
import urllib3
import sys
import subprocess
from configparser import ConfigParser

urllib3.disable_warnings()

parser = ConfigParser()
parser.read('config.ini')

if (len(sys.argv) < 2):
    print("Error, missing arguments")
    print('Args required: python3 script.py "VCSA Username" "VCSA Password"')
    exit(1)

vcsa_url = "https://"+parser.get("VCSA", "vcsa_url")
vcsa_username = sys.argv[1]
vcsa_password = sys.argv[2]


def api_getkey(url, id, password):
    sess = requests.post(url+"/rest/com/vmware/cis/session",
                         auth=(id, password), verify=False)
    sess = json.loads(sess.text)

    try:
        if sess["type"] == "com.vmware.vapi.std.errors.unauthenticated":
            return {"success": False, "message": "No account /  Bad credentials"}
    except:
        return {"success": True, "message": sess['value']}


def user_folder_created(token, username):
    folders = requests.get(vcsa_url+"/rest/vcenter/folder",
                           verify=False, headers={"vmware-api-session-id": token})
    folders = json.loads(folders.text)
    if "type" in folders.keys():
        if folders['type'] == "com.vmware.vapi.std.errors.internal_server_error":
            return False
    else:
        awaited_folder_name = username.lower().split("@")[0]
        for folder in folders['value']:
            if folder['name'] == awaited_folder_name:
                return True
        return False


def user_setup(username):
    subprocess.call(["pwsh", "./sub-scripts/user-setup.ps1", username], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)



user_login = api_getkey(vcsa_url, vcsa_username, vcsa_password)


if(user_login['success']):
    user_token = user_login['message']

    if not(user_folder_created(user_token, vcsa_username)):
        user_setup(vcsa_username)

    result = {
        "success": True, 
        "message": {
            "token": user_token, 
            "username": vcsa_username,
            "password": vcsa_password,
        }
    }
    print(json.dumps(result))

else:
    result = {
        "success": False, 
        "message": "Bad user-token, account not found / bad credentials"
    }
    print(json.dumps(result))
    exit(1)
