# Usage:
# pwsh script.ps1 -vcsa_username USER -vcsa_password PASS -vm_name NAME [opt] -vm_ip IP [opt] -vm_netmask MASK [opt] -vm_gateway GW_IP  [opt] -vm_dns DNS_IP
param ($vcsa_username, $vcsa_password, $vm_name, $vm_ip="0.0.0.0", $vm_netmask="0.0.0.0", $vm_gateway="0.0.0.0", $vm_dns="0.0.0.0")

if ( ($vcsa_username -eq $null) -or ($vcsa_password -eq $null) -or ($vm_name -eq $null) -or ($vm_ip -eq $null) -or ($vm_netmask -eq $null)){
        Write-Host "Missing Args"
        Write-Host "./script.ps1 -vcsa_username USER -vcsa_password PASS -vm_name NAME [opt] -vm_ip IP [opt] -vm_netmask MASK [opt] -vm_gateway GW_IP  [opt] -vm_dns DNS_IP"
        exit 1
}

$pos = $vcsa_username.IndexOf("@")
$base_spec = "W10-Clients"
$template = "W10-Template"
$location = $vcsa_username.Substring(0, $pos)
$datastore = "VMs"
$res_pool = "Cloudis-Cluster"


$config = Get-IniContent "config.ini"
$vcsa_url = $config["VCSA"]["vcsa_url"]

Set-PowerCLIConfiguration -InvalidCertificateAction ignore -Confirm:$false | out-null
Connect-VIServer -Server $vcsa_url -User $vcsa_username -Password $vcsa_password | out-null

Get-OSCustomizationSpec -name $base_spec | New-OSCustomizationSpec -Name tempcust | out-null
Get-OSCustomizationSpec -Name tempcust | Get-OSCustomizationNicMapping | where {$_.Position -eq 2} | Set-OSCustomizationNicMapping -IpMode UseStaticIP -IpAddress $vm_ip -SubnetMask $vm_netmask -DefaultGateway $vm_gateway -Dns $vm_dns | out-null
$final_cust = Get-OSCustomizationSpec -Name tempcust | out-null

New-VM -Name $vm_name -Template $template -OSCustomizationSpec $final_cust -Location $location -Datastore $datastore -ResourcePool $res_pool

Remove-OSCustomizationSpec tempcust -Confirm:$false | out-null

# ./create-vm.ps1 -vcsa_username j.marie@cloudis-girard-presse.lan -vcsa_password Passw0rd. -vm_name "W10 - 001" -vm_ip 172.16.7.1 -vm_netmask 255.255.255.0  -vm_gateway 172.16.7.254 -vm_dns 172.16.10.250