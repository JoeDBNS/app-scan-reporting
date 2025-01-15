param (
    [switch] $preClean = $True,
    [switch] $postClean = $False
)

$dirBundle = "./bundle"
$dirDist = $dirBundle + "/_dist"
$dirWork = $dirBundle + "/tmp"
$dirSpec = $dirBundle + "/spec"


if ($preClean -eq $True) {
    Remove-Item -Path $dirBundle -Recurse
}

# https://pyinstaller.org/en/stable/usage.html
pyinstaller ./src/run_reports.py --name "appscan_srm_reporting" --distpath $dirDist --workpath $dirWork --specpath $dirSpec --onefile --noconfirm

New-Item -Name "src/config" -Path $dirDist + "/" -ItemType Directory

New-Item -Name "logs" -Path $dirDist + "/" -ItemType Directory

Copy-Item "./src/config/main.json" -Destination $dirDist + "/src/config"

if ($postClean -eq $True) {
    Remove-Item -Path $dirWork -Recurse
    Remove-Item -Path $dirSpec -Recurse
}