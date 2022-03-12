import requests
import json
import urllib3
import time
import sys
from configparser import ConfigParser
import subprocess

urllib3.disable_warnings()

parser = ConfigParser()
parser.read('config.ini')

global vcsa_url
vcsa_url = "https://"+parser.get("VCSA", "vcsa_url")

# if (len(sys.argv) < 4):
#     print("Error, missing arguments")
#     print('Args required: python3 script.py "VCSA token" "element" "action"')
#     exit(1)

# vcsa_token = sys.argv[1]
# vcsa_element = sys.argv[2]
# vcsa_action = sys.argv[3]

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
                vm_infos['networks'].append(
                    net['value']['backing']['network_name'])
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

def powershell_setup():
    script = subprocess.Popen(["pwsh","./setup.ps1"])

def user_setup(username):
    script = subprocess.Popen(["pwsh","./create-folder.ps1", username])
    script = subprocess.Popen(["pwsh","./create-network.ps1", username])

def user_vm_create(username, password, vm_name, vm_ip="253", vm_gateway="254", vm_dns="1.1.1.1"):
    script = subprocess.Popen(["pwsh","./create-vm.ps1",username,password,vm_name,vm_ip,vm_gateway,vm_dns])


# powershell_setup()
# user_vm_create("j.marie@cloudis-girard-presse.lan", "Passw0rd.", "marie-python-vm" ,"150", "254", "8.8.8.8")

print(json.dumps(user_get_vms("2b2f8fe9b54a45fed515a157c5e9e140"),indent=2))

# print(json.dumps(user_folder_created(user_token, vcsa_username), indent=2))

# New-VM -Name 'W10-001' -Template $(Get-Template -Name "W10-Template")  -OSCustomizationSpec $(Get-OSCustomizationSpec -Name "W10-Clients") -VMHost $(Get-Folder "Clients") -Datastore 'VMs'