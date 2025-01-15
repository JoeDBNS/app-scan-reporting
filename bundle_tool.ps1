param (
    [switch] $preClean = $False,
    [switch] $postClean = $False,
    [switch] $buildZip = $False
)

$projectName = "appscan_srm_reporting"
$dirBundle = "./bundle"
$dirDist = $dirBundle + "/_dist"
$dirWork = $dirBundle + "/tmp"
$dirSpec = $dirBundle + "/spec"


if ($preClean) {
    if (Test-Path -Path $dirBundle) {
        Remove-Item -Path $dirBundle -Recurse
    }
}

# https://pyinstaller.org/en/stable/usage.html
pyinstaller ./src/run_reports.py --name $projectName --distpath $dirDist --workpath $dirWork --specpath $dirSpec --onefile --noconfirm

New-Item -Name "src/config" -Path ($dirDist + "/") -ItemType Directory
New-Item -Name "_logs" -Path ($dirDist + "/") -ItemType Directory

if (Test-Path -Path "./src/config/main.json") {
    Copy-Item "./src/config/main.json" -Destination ($dirDist + "/src/config")
}
else {
    Write-Output "main.json file not found."
}


if ($postClean) {
    if (Test-Path -Path $dirWork) {
        Remove-Item -Path $dirWork -Recurse
    }
    if (Test-Path -Path $dirSpec) {
        Remove-Item -Path $dirSpec -Recurse
    }
}

if ($buildZip) {
    # Compress-Archive ignores empty folders.
    New-Item -Path ($dirDist + "/_logs") -Name ".keep" -ItemType "file" -Value ""

    $compress = @{
        Path = ($dirDist + "/*")
        CompressionLevel = "Fastest"
        DestinationPath = ($dirBundle + "\" + $projectName + ".zip")
    }
    Compress-Archive @compress -Force
}