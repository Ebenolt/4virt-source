# Save a user vm
# ./script.ps1 -vcsa_username USER -vcsa_password PASS -vm_id ID


param ($vcsa_username, $vcsa_password, $vm_id)

if ( ($vcsa_username -eq $null) -or ($vcsa_password -eq $null) -or ($vm_id -eq $null)) {
        Write-Host "Missing Args"
        Write-Host "./script.ps1 -vcsa_username USER -vcsa_password PASS -vm_id ID"
        exit 1
}


$date = Get-Date -Format "yyyyMMdd"
$time = Get-Date -f "HH:m:ss"
$pretty_date = Get-Date -Format "dd-MM-yyyy"


$config = Get-IniContent "config.ini"
$vcsa_url = $config["VCSA"]["vcsa_url"]
$backup_path = $config["VCSA"]["backup_store"]
$clone_name = "Clone-Snapshot"

Set-PowerCLIConfiguration -InvalidCertificateAction ignore -Confirm:$false | out-null
Connect-VIServer -Server $vcsa_url -User $vcsa_username -Password $vcsa_password | out-null


$vm = Get-VM -Id "VirtualMachine-$vm_id"
$vm_name = $vm.name

New-Snapshot -Name $clone_name -VM $vm_name -Confirm:$false -RunAsync

Start-Sleep -Seconds 10

$vmView = $vm | Get-View

$cloneFolder = $vmView.parent

$cloneSpec = new-object Vmware.Vim.VirtualMachineCloneSpec
$cloneSpec.Snapshot = $vmView.Snapshot.CurrentSnapshot

$cloneSpec.Location = new-object Vmware.Vim.VirtualMachineRelocateSpec
$cloneSpec.Location.Datastore = (Get-Datastore -Name $backup_path | Get-View).MoRef
$cloneSpec.Location.Transform =  [Vmware.Vim.VirtualMachineRelocateTransformation]::sparse

$cloneName = "bkp_$vm-$date-$time"

$vmView.CloneVM( $cloneFolder, $cloneName, $cloneSpec )

Get-Snapshot -VM (Get-VM -Name $vm_name) -Name $clone_name | Remove-Snapshot -confirm:$False -RunAsync

& ./sub-scripts/mail.ps1 "VM Backup" "VM $vm_name has been backuped at $pretty_date / $time" me@ebenolt.com | out-null