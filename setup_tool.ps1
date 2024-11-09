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
}