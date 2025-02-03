param (
    [string] $pathChoice = ""
)


Write-Host @"

 _____          _____         _____           _____
|   __|        |  _  |       | __  |         |   __|
|   __|        |     |       |    -|         |__   |
|_____|xtended |__|__|ppScan |__|__|eporting |_____|uite

--------------------------------------------------------
"@ -ForegroundColor Green


$pathOptions = @("admin", "reports")

while (-not ($pathChoice -in $pathOptions)) {
    $pathChoice = Read-Host "`n`nDo you want to run [admin] or [reports]?" | ForEach-Object { $_.ToLower().Trim() }

    if (-not ($pathChoice -in $pathOptions)) {
        Write-Host "Invalid entry" -ForegroundColor Red
    }
}

Switch ($pathChoice)
{
    "admin" {
        python './src/run_admin.py'
    }
    "reports" {
        python './src/run_reports.py'
    }
}
