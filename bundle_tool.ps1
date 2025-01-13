# https://pyinstaller.org/en/stable/usage.html
pyinstaller ./src/run_reports.py --name "appscan_srm_reporting" --distpath "./bundle/dist" --workpath "./bundle/tmp" --specpath "./bundle/spec" --onefile --noconfirm

New-Item -Name "src/config" -Path "./bundle/dist/" -ItemType Directory

Copy-Item "./src/config/main.json" -Destination "./bundle/dist/src/config"

Read-Host "Press Enter to close"