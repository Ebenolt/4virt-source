# Attach a VM to user network
# ./script.ps1 -vm_name VM -username USER

param ($vm_name, $username)

if ( ($vm_name -eq $null) -or ($username -eq $null) ){
        Write-Host "Missing Args"
        Write-Host "./script.ps1 -vm VM_Name -username USER_NAME"
        exit 1
}

$config = Get-IniContent "config.ini"
$vcsa_url = $config["VCSA"]["vcsa_url"]
$vcsa_admin_username = $config["VCSA"]["vcsa_admin_username"]
$vcsa_admin_password = $config["VCSA"]["vcsa_admin_password"]

$pos = $username.IndexOf("@")
$network = $username.Substring(0, $pos)

Set-PowerCLIConfiguration -InvalidCertificateAction ignore -Confirm:$false | out-null
Connect-VIServer -Server $vcsa_url -User $vcsa_admin_username -Password $vcsa_admin_password | out-null



New-NetworkAdapter -vm $vm_name -Portgroup $network -Type "VMXNET3" -startconnected | out-null