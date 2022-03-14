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

howto = 'script.py --username(-u) <vcsa_username> --password(-p) <vcsa_password> --token(-t) <vcsa_token> --action(-a) <action> --element(-e) <element_id>'

try:
    opts, args = getopt.getopt(sys.argv[1:],"hu:p:t:a:e:n:i:g:d:",["username=","password=", "token=", "action=", "id=", "vm_name=", "vm_ip=", "vm_gateway=", "vm_dns="])

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
    test = api_makerequest(vcsa_url+"/rest/vcenter/vm", token)
    if "type" in test.keys():
        if test['type'] == "com.vmware.vapi.std.errors.unauthenticated":
            return False
        else:
            return True
    else:
        return True

def powershell_setup():
    script = subprocess.Popen(["pwsh","./setup.ps1"])

def user_setup(username):
    script = subprocess.Popen(["pwsh","./user-setup.ps1", username])

def user_get_vms(token):
    if(user_valid_token(token)):
        vms = api_makerequest(vcsa_url+"/rest/vcenter/vm", token)
        vms_list = []
        for vm in vms['value']:
            vm_detail = api_makerequest(
                vcsa_url+"/rest/vcenter/vm/"+vm['vm'], token)
            try:
                vm_ip = api_makerequest(
                    vcsa_url+"/rest/vcenter/vm/"+vm['vm']+"/guest/identity/", token)['value']['ip_address']
            except:
                vm_ip = "Unknown"
            vm_infos = {"id": vm['vm'],
                        "name": vm_detail['value']['name'],
                        "status": vm_detail['value']['power_state'],
                        "cpu": vm['cpu_count'],
                        "ram": vm['memory_size_MiB'],
                        "ip": vm_ip,
                        "last_backup": "",
                        "networks": []}
            for net in vm_detail['value']['nics']:
                try:
                    vm_infos['networks'].append(net['value']['backing']['network_name'])
                except:
                    pass
            vms_list.append(vm_infos)

        result = vms_list
        return result
    else:
        return {"success": False, "message": "Bad / Missing token"}

def user_stop_vm(token, id):
    if(user_valid_token(token)):
        vm_stop = api_makerequest(vcsa_url+"/rest/vcenter/vm/"+id+"/power/stop",
                                  token,
                                  "POST")

        if "type" in vm_stop.keys():
            if vm_stop['type'] == "com.vmware.vapi.std.errors.already_in_desired_state":
                return {"success": False, "message": vm_stop['value']['messages'][0]['default_message']}

        return vm_stop

def user_start_vm(token, id):
    if(user_valid_token(token)):
        vm_start = api_makerequest(vcsa_url+"/rest/vcenter/vm/"+id+"/power/start",
                                   token,
                                   "POST")

        if "type" in vm_start.keys():
            if vm_start['type'] == "com.vmware.vapi.std.errors.already_in_desired_state":
                return {"success": False, "message": vm_start['value']['messages'][0]['default_message']}

        return vm_start

def user_reset_vm(token, id):
    if(user_valid_token(token)):
        vm_reset = api_makerequest(vcsa_url+"/rest/vcenter/vm/"+id+"/power/reset",
                                   token,
                                   "POST")

        if "type" in vm_reset.keys():
            if vm_reset['type'] == "com.vmware.vapi.std.errors.already_in_desired_state":
                return {"success": False, "message": vm_reset['value']['messages'][0]['default_message']}

        return vm_reset

def user_suspend_vm(token, id):
    if(user_valid_token(token)):
        vm_suspend = api_makerequest(vcsa_url+"/rest/vcenter/vm/"+id+"/power/suspend",
                                     token,
                                     "POST")

        if "type" in vm_suspend.keys():
            if vm_suspend['type'] == "com.vmware.vapi.std.errors.already_in_desired_state":
                return {"success": False, "message": vm_suspend['value']['messages'][0]['default_message']}

        return vm_suspend

def user_delete_vm(token, id):
    if(user_valid_token(token)):
        vm_detail = api_makerequest(vcsa_url+"/rest/vcenter/vm/"+id, token)
        if "type" in vm_detail.keys():
            if vm_detail['type'] == "com.vmware.vapi.std.errors.not_found":
                return {"success": False, "message": "Non-existant / Not created VM"}

        vm_deletion = api_makerequest(
            vcsa_url+"/rest/vcenter/vm/"+id, token, "DELETE")

        if "type" in vm_deletion.keys():
            if vm_deletion['type'] == "com.vmware.vapi.std.errors.not_allowed_in_current_state":
                return {"success": False, "message": vm_deletion['value']['messages'][0]['default_message']}

        result = vm_deletion
        return result
    else:
        return {"success": False, "message": "Bad / Missing token"}

def user_vm_create(username, password, vm_name, vm_ip="253", vm_gateway="254", vm_dns="1.1.1.1"):
    script = subprocess.Popen(["pwsh","./sub-scripts/create-vm.ps1",username,password,vm_name,vm_ip,vm_gateway,vm_dns], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


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