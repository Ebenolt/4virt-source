# ./create-vm.ps1 -vcsa_username j.dupont@cloudis-girard-presse.lan -vcsa_password Passw0rd. -vm_name "W10-Test-001-dupont" -vm_ip "192.168.5.150" -vm_gateway "192.168.5.254" -vm_dns "1.1.1.1"
param ($vcsa_username, $vcsa_password, $vm_name, $vm_ip="192.168.254.253", $vm_gateway="192.168.254.254", $vm_dns="1.1.1.1")

if ( ($vcsa_username -eq $null) -or ($vcsa_password -eq $null) -or ($vm_name -eq $null) -or ($vm_ip -eq $null)) {
        Write-Host "Missing Args"
        Write-Host "./script.ps1 -vcsa_username USER -vcsa_password PASS -vm_name NAME [opt] -vm_ip IP [opt] -vm_gateway = GW [opt] -vm_dns = DNS"
        exit 1
}

$vcsa_url = $config["VCSA"]["vcsa_url"]

Set-PowerCLIConfiguration -InvalidCertificateAction ignore -Confirm:$false | out-null
Connect-VIServer -Server $vcsa_url -User $vcsa_username -Password $vcsa_password | out-null


$pos = $vcsa_username.IndexOf("@")
$uname = $vcsa_username.Substring(0, $pos)
$template = Get-Template -Name "W10-Template"
$base_spec = "W10-Clients"
$datastore = "VMs"
$res_pool = "Cloudis-Cluster"
$config = Get-IniContent "config.ini"


$spec_clone = Get-OSCustomizationSpec -Name W10-Clients | New-OSCustomizationSpec -Name WindowsTemp -Type NonPersistent

$nicMapping = Get-OSCustomizationNicMapping –OSCustomizationSpec $spec_clone | Where { $_.position -eq 2 }

$nicMapping | Set-OSCustomizationNicMapping –IpMode UseStaticIP –IpAddress $vm_ip –SubnetMask “255.255.255.0” –DefaultGateway $vm_gateway -Dns $vm_dns

$vm_task = New-VM -Name $vm_name -Template $template -OSCustomizationSpec WindowsTemp -ResourcePool $res_pool -Datastore $datastore -DiskStorageFormat Thin -Location $uname -RunAsync

$task_id = $vm_task.id

while ($vm_task.PercentComplete -lt 100)
{
    Start-Sleep -Seconds 2
    $vm_task = Get-Task -Id $task_id
}


Remove-OSCustomizationSpec WindowsTemp -Confirm:$false | out-null

Get-VM $vm_name | Get-NetworkAdapter -Name "Network adapter 2" | Set-NetworkAdapter -NetworkName $uname -Confirm:$false -StartConnected:$True | out-null

$vm = Start-VM $vm_name -Confirm:$false | out-null