# Setup user environment (Network and folder)
# Usage: ./script.ps1 -username USER 


param ($username)

if ( ($username -eq $null) ){
        Write-Host "Missing Args"
        Write-Host "./script.ps1 -username USER"
        exit 1
}


$config = Get-IniContent "config.ini"
$vcsa_url = $config["VCSA"]["vcsa_url"]
$vcsa_admin_username = $config["VCSA"]["vcsa_admin_username"]
$vcsa_admin_password = $config["VCSA"]["vcsa_admin_password"]

Set-PowerCLIConfiguration -InvalidCertificateAction ignore -Confirm:$false | out-null
Connect-VIServer -Server $vcsa_url -User $vcsa_admin_username -Password $vcsa_admin_password | out-null

$pos = $username.IndexOf("@")
$uname = $username.Substring(0, $pos)

$folders = Get-Folder
$networks = Get-VDPortgroup

if ( -Not ($folders.Name -contains $uname )){
    New-Folder -Name $uname -Location $(Get-Folder "Clients") | out-null
    Get-Folder $uname | New-VIPermission -Role 'Domain_Users' -Principal "CLOUDIS\$($uname)" | out-null
}

if ( -Not ($networks.Name -contains $uname )){
    New-VDPortgroup -Name $uname -VDSwitch "Production DSwitch" | out-null
    Get-VDPortgroup -Name $uname | New-VIPermission -Role 'Domain_Users' -Principal "CLOUDIS\$($uname)" | out-null
}