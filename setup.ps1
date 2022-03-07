Install-Module PsIni
Install-Module -Name VMware.PowerCLI -Scope CurrentUser
Set-PowerCLIConfiguration -Scope User -ParticipateInCEIP $false -Confirm:$false