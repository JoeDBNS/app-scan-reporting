Remove-Item -Path "./bundle" -Recurse

# https://pyinstaller.org/en/stable/usage.html
pyinstaller ./src/run_reports.py --name "appscan_srm_reporting" --distpath "./bundle/_dist" --workpath "./bundle/tmp" --specpath "./bundle/spec" --onefile --noconfirm

New-Item -Name "src/config" -Path "./bundle/_dist/" -ItemType Directory

Copy-Item "./src/config/main.json" -Destination "./bundle/_dist/src/config"