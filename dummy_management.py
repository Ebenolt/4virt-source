# Usage: python3 script.py username@domain password
# Central management script

import requests
import json
import urllib3
import time
import sys
import getopt
from configparser import ConfigParser
import subprocess
urllib3.disable_warnings()


vcsa_username = ''
vcsa_password = ''
vcsa_token = ''
element_id = ''
action = ''

vm_name = ''
vm_ip = ''
vm_gateway = ''
vm_dns = ''
global success
success = True

howto = 'script.py --fail(-f) --username(-u) <vcsa_username> --password(-p) <vcsa_password> --token(-t) <vcsa_token> --action(-a) <action> --element(-e) <element_id>'

try:
    opts, args = getopt.getopt(sys.argv[1:],"hu:p:t:a:e:n:i:g:d:f",["username=","password=", "token=", "action=", "id=", "vm_name=", "vm_ip=", "vm_gateway=", "vm_dns=", "fail="])

except getopt.GetoptError:
    print (howto)
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print (howto)
        sys.exit()
    elif opt in ("-u", "--username"):
        vcsa_username = arg
    elif opt in ("-p", "--password"):
        vcsa_password = arg
    elif opt in ("-t", "--token"):
        vcsa_token = arg
    elif opt in ("-a", "--action"):
        action = arg
    elif opt in ("-e", "--element"):
        element_id = arg
    elif opt in ("-n", "--vm_name"):
        vm_name = arg
    elif opt in ("-i", "--vm_ip"):
        vm_ip = arg
    elif opt in ("-g", "--vm_gateway"):
        vm_gateway = arg
    elif opt in ("-d", "--vm_dns"):
        vm_dns = arg
    elif opt in ("-f", "--fail"):
        success = False

if ( '' in [vcsa_username, vcsa_password, vcsa_token, action] ):
    print("Missing args, usage:")
    print(howto)
    exit(1)

parser = ConfigParser()
parser.read('config.ini')

global vcsa_url
vcsa_url = "https://"+parser.get("VCSA", "vcsa_url")


def api_makerequest(url, token, method="GET", aditionnals_headers={}):
    request_headers = {
        "vmware-api-session-id": token
    }

    for header, value in aditionnals_headers.items():
        request_headers[header] = value

    if method == "GET":
        request = requests.get(url, verify=False, headers=request_headers)
    elif method == "POST":
        request = requests.post(url, verify=False, headers=request_headers)
    elif method == "DELETE":
        request = requests.delete(url, verify=False, headers=request_headers)
    else:
        return {"success": False, "message": "Bad method: "+method}

    try:
        request_json = json.loads(request.text)
        return request_json
    except:
        return {"success": True, "message": ""}


def user_valid_token(token):
    return True

def powershell_setup():
    pass

def user_setup(username):
    pass

def user_get_vms(token):
    if(user_valid_token(token)):
        result = json.dumps({
                                "success":True,
                                "message":[
                                    {
                                        "id": "vm-19",
                                        "name": "VMware vCenter Server Appliance",
                                        "status": "POWERED_ON",
                                        "cpu": 2, "ram": 10240,
                                        "ip": "192.168.11.30",
                                        "backups": [],
                                        "networks": [
                                            "VMs Management Network"
                                        ]
                                    },
                                    {
                                        "id": "vm-273",
                                        "name": "Test-005",
                                        "status": "POWERED_OFF",
                                        "cpu": 2,
                                        "ram": 3072,
                                        "ip": "Unknown",
                                        "backups": [
                                            "15_03_2022-15:41:03",
                                            "15_03_2022-15:43:21",
                                            "15_03_2022-15:46:25",
                                            "15_03_2022-16:17:41"
                                        ],
                                        "networks": [
                                            "Public Network"
                                        ]
                                    }
                                ]
                            })
        return result
    else:
        return {"success": False, "message": "Bad / Missing token"}

def user_stop_vm(token, id):
    if success:
        return {"success": True, "message": "VM stopped !"}
    else:
        return {"success": False, "message": "Can't stop VM"}

def user_start_vm(token, id):
    if success:
        return {"success": True, "message": "VM started !"}

    else:
        return {"success": False, "message": "Can't start VM"}

def user_reset_vm(token, id):
    if success:
        return {"success": True, "message": "VM restarted !"}
    else:
        return {"success": False, "message": "Can't reset VM"}


def user_suspend_vm(token, id):
    if success:
        return {"success": True, "message": "VM suspended !"}
    else:
        return {"success": False, "message": "Can't suspend VM"}


def user_delete_vm(token, id):
    if success:
        return {"success": True, "message": "VM deleted !"}
    else:
        return {"success": False, "message": "Can't delete VM"}

def user_vm_create(username, password, vm_name, vm_ip="253", vm_gateway="254", vm_dns="1.1.1.1"):
    if success:
        return {"success": True, "message": "VM created !"}
    else:
        return {"success": False, "message": "Can't suspend VM"}   


if action == "get":
    print(json.dumps(user_get_vms(vcsa_token)))
elif action in ["stop", "start", "reset", "suspend", "delete"]:
    if element_id == "":
        result = {"success": False,
            "message": "Missing arg --id(-i)",
            "howto":howto
            }
        print(json.dumps(result))
    else:
        if action == "start":
            print(json.dumps(user_start_vm(vcsa_token, element_id)))
        elif action == "stop":
            print(json.dumps(user_stop_vm(vcsa_token, element_id)))
        elif action == "reset":
            print(json.dumps(user_reset_vm(vcsa_token, element_id)))
        elif action == "suspend":
            print(json.dumps(user_suspend_vm(vcsa_token, element_id)))
        elif action == "delete":
            print(json.dumps(user_delete_vm(vcsa_token, element_id)))
elif action == "create":
    if "" in [vm_name, vm_ip, vm_gateway, vm_dns]:
        result = {"success": False,
            "message": "Missing args",
            "howto":howto[:-26] + "--vm_name(-n) <vm_name> --vm_ip(-i) <vm_last_ip_block> --vm_gateway(-g) <gateway_last_ip_block> --vm_dns(-d) <dns_ip>"
            }
        print(json.dumps(result))
    else:
        user_vm_create(vcsa_username, vcsa_password, vm_name ,vm_ip, vm_gateway, vm_dns)
        result = {"success": True,
            "message": "VM Created !"
            }
        print(json.dumps(result))
else:
    result = {"success": False,
                "message": "Action arg not recognized (start, stop, reset, suspend, delete, create)",
                "howto":howto
                }
    print(json.dumps(result))