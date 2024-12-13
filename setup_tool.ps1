function Install-Local-BuildTools {
    # https://learn.microsoft.com/en-us/answers/questions/192162/visual-studio-build-tools-silent-install
}

function Install-Local-Choco {
    # https://chocolatey.org/install#individual
    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

function Install-Local-Python {
    choco install -y python3
}

function Install-Local-Python-Deps {
    pip install requests
    pip install openpyxl
    pip install py7zr
}


try {
    choco -v
    Write-Host "`nChocolately Found" -ForegroundColor Green

    try {
        python --version
        Write-Host "`nPython Found" -ForegroundColor Green

        try {
            Install-Local-Python-Deps
        }
        catch {
            Write-Host "`n! - pip Dependency Install Errors" -ForegroundColor Red
        }
    }
    catch {
        try {
            Install-Local-Python

            python --version | Write-Host -ForegroundColor Green

            try {
                Install-Local-Python-Deps
            }
            catch {
                Write-Host "`n! - pip Dependency Install Errors" -ForegroundColor Red
            }
        }
        catch {
            Write-Host "`n! - Python Install Error" -ForegroundColor Red
        }
    }
}
catch {
    Write-Host "`n! - Chocolately Not Found" -ForegroundColor Red

    try {
        Install-Local-Choco

        try {
            choco -v
            Write-Host "`nChocolately Installed Successfully" -ForegroundColor Green

            try {
                python --version
                Write-Host "`nPython Found" -ForegroundColor Green

                try {
                    Install-Local-Python-Deps
                }
                catch {
                    Write-Host "`n! - pip Dependency Install Errors" -ForegroundColor Red
                }
            }
            catch {
                try {
                    Install-Local-Python

                    python --version | Write-Host -ForegroundColor Green

                    try {
                        Install-Local-Python-Deps
                    }
                    catch {
                        Write-Host "`n! - pip Dependency Install Errors" -ForegroundColor Red
                    }
                }
                catch {
                    Write-Host "`n! - Python Install Error" -ForegroundColor Red
                }
            }
        }
        catch {
            Write-Host "`n! - Chocolately Install Failure" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "`n! - Chocolately Install Error" -ForegroundColor Red
    }
}




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
        "reports": [
            {
                "type": "",
                "contacts": [
                    {
                        "role": "",
                        "name": "",
                        "emails": [],
                        "secure-delivery": {
                            "7zip": false,
                            "password": ""
                        }
                    }
                ]
            }
        ]
    }
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

Read-Host "`n`nPress Enter to close."