Install-Module PsIni -Scope AllUsers
Install-Module -Name VMware.PowerCLI -Scope AllUsers
Set-PowerCLIConfiguration -Scope AllUsers -ParticipateInCEIP $false -Confirm:$false
