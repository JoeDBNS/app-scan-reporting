# AppScan-SRM-Reporting


## Run Scripts

### Setup Tool:

``` PowerShell
Powershell.exe -ExecutionPolicy Bypass -File ".\setup_tool.ps1"
```

### Execute Tool:

``` PowerShell
Powershell.exe -ExecutionPolicy Bypass -File ".\run_reports.ps1"
```





## Planned Features:
- Management CLI for config file
- .xlsx improvements
  - Charts and Graphs
- Execution result logs
- Scheduling reports and schedule management CLI
- Add filtering to search to exclude results already marked as resolved in some way

## Possible Features:
- Translate to NodeJS for greater ability to run from anywhere and without admin rights [excel4node](https://www.npmjs.com/package/excel4node)
