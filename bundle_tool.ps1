param (
    [switch] $preClean = $True,
    [switch] $postClean = $False,
    [switch] $buildZip = $False
)

$projectName = "appscan_srm_reporting"
$dirBundle = "./bundle"
$dirDist = $dirBundle + "/_dist"
$dirWork = $dirBundle + "/tmp"
$dirSpec = $dirBundle + "/spec"


if (Test-Path -Path $dirBundle) {
    if ($preClean -eq $True) {
        Remove-Item -Path $dirBundle -Recurse
    }
}

# https://pyinstaller.org/en/stable/usage.html
pyinstaller ./src/run_reports.py --name $projectName --distpath $dirDist --workpath $dirWork --specpath $dirSpec --onefile --noconfirm

New-Item -Name "src/config" -Path ($dirDist + "/") -ItemType Directory
New-Item -Name "logs" -Path ($dirDist + "/") -ItemType Directory

Copy-Item "./src/config/main.json" -Destination ($dirDist + "/src/config")

if ($postClean -eq $True) {
    Remove-Item -Path $dirWork -Recurse
    Remove-Item -Path $dirSpec -Recurse
}

if ($buildZip -eq $True) {
    # Compress-Archive ignores empty folders.
    New-Item -Path ($dirDist + "/logs") -Name ".keep" -ItemType "file" -Value ""

    $compress = @{
        Path = ($dirDist + "/*")
        CompressionLevel = "Fastest"
        DestinationPath = ($dirBundle + "\" + $projectName + ".zip")
    }
    Compress-Archive @compress -Force
}