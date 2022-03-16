# Save a user vm
# ./script.ps1 -subject SUBJECT -body BODY -to TO_EMAIL


param ($subject, $body, $to)

if ( ($subject -eq $null) -or ($body -eq $null) -or ($to -eq $null)) {
        Write-Host "Missing Args"
        Write-Host "./script.ps1 -subject SUBJECT -body BODY"
        exit 1
}

Import-Module PsIni


$config = Get-IniContent "config.ini"
$mail_username = $config["Mail"]["username"]
$mail_password = $config["Mail"]["password"]
$mail_server = $config["Mail"]["server"]
$mail_port = $config["Mail"]["port"]



$body = @{
    server_username = $mail_username
    server_password = $mail_password
    server_name = $mail_server
    server_port = $mail_port
    mail_from = "VCSA Mailer"
    mail_to = $to
    mail_subject = $subject
    mail_body = $body
}
$json_body = $body | ConvertTo-Json

Invoke-RestMethod -Method POST -Uri https://mailer.ebe.ovh/v1/send/  -body $json_body
