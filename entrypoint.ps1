param (
    [string] $pathChoice = ""
)

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
        Write-Host "!! - admin - !!"
    }
    "reports" {
        Write-Host "!! - reports - !!"
    }
}