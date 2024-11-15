pip install openpyxl

$config_text = @'
{
    "smtp": {
        "host": "",
        "port": 0,
        "sender": {
            "name": "",
            "email": ""
        }
    },
    "hosts": {
        "internal-network": "",
        "srm": ""
    },
    "secret-token": "",
    "projects": [
        {
            "id": 0,
            "name": "",
            "contacts": [
                {
                    "role": "",
                    "name": "",
                    "email": ""
                }
            ]
        }
    ]
}
'@

if (!(Test-Path './src/config/main.json')) {
    New-Item './src/config/main.json' -value $config_text
    Write-Host "`n"
    Write-Host "'main.json' File Created" -ForegroundColor "Green"
}
else {
    Write-Host "`n"
    Write-Host "'main.json' File Already Exists" -ForegroundColor "Green"
}