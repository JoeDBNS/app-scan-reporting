# AppScan-SRM-Reporting


## Run Scripts

### Load Dependencies:

``` PowerShell
Powershell.exe -ExecutionPolicy Bypass -File ".\setup_dev.ps1"
```

### Execute Tool:

``` PowerShell
Powershell.exe -ExecutionPolicy Bypass -File ".\run_reports.ps1"
```

### Compile Tool as .exe:

``` PowerShell
Powershell.exe -ExecutionPolicy Bypass -File ".\bundle_tool.ps1" --postClean $True
```





## Planned Features:
- Management CLI for config file
- .xlsx improvements
  - Charts and Graphs
    - Pie chart for finding tool
    - Pie chart for finding severity
    - Line graph for date found
- Execution result logs
- Scheduling reports and schedule management CLI

## Possible Features:
- Translate to NodeJS for greater ability to run from anywhere and without admin rights [excel4node](https://www.npmjs.com/package/excel4node)
