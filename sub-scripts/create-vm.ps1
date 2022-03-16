# Create a VM in user folder, attach it to user network, defining IP domain etc... then starting it
# ./script.ps1 -vcsa_username USER -vcsa_password PASS -vm_name VM -vm_ip LAST_IP_BLOCK -vm_gateway LAST_IP_GATEWAY -vm_dns DNS
# Opt: vm_ip, vm_gateway, vm_dns

param ($vcsa_username, $vcsa_password, $vm_name, $vm_ip="253", $vm_gateway="254", $vm_dns="1.1.1.1")

if ( ($vcsa_username -eq $null) -or ($vcsa_password -eq $null) -or ($vm_name -eq $null) -or ($vm_ip -eq $null)) {
        Write-Host "Missing Args"
        Write-Host "./script.ps1 -vcsa_username USER -vcsa_password PASS -vm_name NAME [opt] -vm_ip IP [opt] -vm_gateway = GW [opt] -vm_dns = DNS"
        exit 1
}

$config = Get-IniContent "config.ini"
$vcsa_url = $config["VCSA"]["vcsa_url"]

Set-PowerCLIConfiguration -InvalidCertificateAction ignore -Confirm:$false | out-null
Connect-VIServer -Server $vcsa_url -User $vcsa_username -Password $vcsa_password | out-null


$pos = $vcsa_username.IndexOf("@")
$uname = $vcsa_username.Substring(0, $pos)
$template_name = $config["VCSA"]["template_name"]
$template = Get-Template -Name $template_name
$base_spec = $config["VCSA"]["base_spec"]
$datastore = $config["VCSA"]["datastore"]
$res_pool = $config["VCSA"]["res_pool"]


[regex]$regex = "[0-9]+"
$folder_id = $(Get-Folder -name $uname).id
$vlan_id = $regex.Matches($folder_id) | foreach-object {$_.Value}
$full_ip = "192.168." + $vlan_id + "."+$vm_ip
$full_gateway = "192.168." + $vlan_id + "."+$vm_gateway


$spec_clone = Get-OSCustomizationSpec -Name $base_spec | New-OSCustomizationSpec -Name WindowsTemp -Type NonPersistent

$nicMapping = Get-OSCustomizationNicMapping –OSCustomizationSpec $spec_clone | Where { $_.position -eq 2 }

$nicMapping | Set-OSCustomizationNicMapping –IpMode UseStaticIP –IpAddress $full_ip –SubnetMask “255.255.255.0” –DefaultGateway $full_gateway -Dns $vm_dns

$vm_task = New-VM -Name $vm_name -Template $template -OSCustomizationSpec WindowsTemp -ResourcePool $res_pool -Datastore $datastore -Location $uname -RunAsync

$task_id = $vm_task.id

while ($vm_task.PercentComplete -lt 100)
{
    Start-Sleep -Seconds 2
    $vm_task = Get-Task -Id $task_id
}



Remove-OSCustomizationSpec WindowsTemp -Confirm:$false | out-null

$port_group = Get-VDPortGroup -Name $uname

Get-VM $vm_name | Get-NetworkAdapter -Name "Network adapter 2" | Set-NetworkAdapter -Portgroup $port_group -Confirm:$false | out-null

Get-VM $vm_name | Get-NetworkAdapter -Name "Network adapter 2" | Set-NetworkAdapter -Connected:$true -Confirm:$false | out-null


$vm = Start-VM $vm_name -Confirm:$false | out-null