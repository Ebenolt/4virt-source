Setup:
# Install-Module PsIni
# Install-Module -Name VMware.PowerCLI -Scope CurrentUser
# Set-PowerCLIConfiguration -Scope User -ParticipateInCEIP $false -Confirm:$false


$username = $args[0]

$config = Get-IniContent "config.ini"
$vcsa_url = $config["VCSA"]["vcsa_url"]
$vcsa_admin_username = $config["VCSA"]["vcsa_admin_username"]
$vcsa_admin_password = $config["VCSA"]["vcsa_admin_password"]


Set-PowerCLIConfiguration -InvalidCertificateAction ignore -Confirm:$false | out-null

Connect-VIServer -Server $vcsa_url -User $vcsa_admin_username -Password $vcsa_admin_password | out-null

New-Folder -Name $username -Location (Get-Folder "Clients") | out-null

Get-Folder $username | New-VIPermission -Role 'Domain_User' -Principal "CLOUDIS\$($username)" | out-null