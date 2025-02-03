````
 _____          _____         _____           _____
|   __|        |  _  |       | __  |         |   __|
|   __|        |     |       |    -|         |__   |
|_____|xtended |__|__|ppScan |__|__|eporting |_____|uite
````


# Extended AppScan Reporting Suite

&nbsp;
&nbsp;

## Run Scripts

### Load Dependencies:

``` PowerShell
Powershell.exe -ExecutionPolicy Bypass -File ".\setup_dev.ps1"
```

### Execute Reporting Tool:

``` PowerShell
Powershell.exe -ExecutionPolicy Bypass -File ".\entrypoint.ps1" --pathChoice "reports"
```

### Compile Tool as .exe:

``` PowerShell
Powershell.exe -ExecutionPolicy Bypass -File ".\bundle_tool.ps1" --preClean --postClean --buildZip
```





## Planned Features:
- Management CLI for config file
- .xlsx improvements
  - Charts and Graphs
    - Pie chart for finding tool
    - Pie chart for finding severity
    - Line graph for date found
- Scheduling reports and schedule management CLI
- Improve CLI use with tools like curses or pick [pypi.org/project/pick](https://pypi.org/project/pick/)
  - Additional resources here ([github.com/shadawck/awesome-cli-frameworks](https://github.com/shadawck/awesome-cli-frameworks?tab=readme-ov-file#python))
