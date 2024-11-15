choco -v

# @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"

choco install -y python3

python --version

pip install openpyxl
pip install requests

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
                    "emails": []
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

Read-Host "Press Enter to close."