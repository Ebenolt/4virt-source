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
    return {"success": True, "message": "3bc2c6601e27a9075d43977984684d6a"}


def user_folder_created(token, username):
    return False


def user_setup(username):
    pass



user_login = api_getkey(vcsa_url, vcsa_username, vcsa_password)


if(user_login['success']):
    user_token = user_login['message']
    result = {
        "success": True, 
        "message": {
            "token": user_token, 
            "username": vcsa_username,
            "password": vcsa_password,
        }
    }
    print(json.dumps(result))