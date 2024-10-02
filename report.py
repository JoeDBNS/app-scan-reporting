import json, requests
import xlsx_maker as xm


# Load config json from local config.json file
def LoadConfigFile():
    try:
        with open('./config/main.json') as file:
            return json.load(file)
    except:
        print('ERROR - LoadConfigFile()')
        return False


# Build URL string for specific SRM finding/result/issue
def BuildIssueUrl(project_id, issue_id):
    return config['hosts']['srm'] + '/projects/' + str(project_id) + '/findings/' + str(issue_id)


# Build string from issue source path array list
def BuildFindingPathString(path):
    path_as_string = path[0]

    for item in path[1:]:
        path_as_string += ' - ' + item

    return path_as_string



def GetProjectList():
    try:
        projects_request_url = config['hosts']['srm'] + '/api/projects'

        projects_request = requests.get(projects_request_url, headers={'Content-Type':'application/json', 'API-Key':config['secret-token']})
        projects_response_data = json.loads(projects_request.text)

    except:
        projects_response_data = []
        print('ERROR - GetProjectList()')

    return projects_response_data['projects']



def GetProjectFindings(project_id):
    try:
        project_request_url = config['hosts']['srm'] + '/api/projects/' + str(project_id) + '/findings/table?expand=results,triage-time'

        project_request_data = {
            'filter': {
                'severity': ['High', 'Medium', 'Low']
            },
            'sort': {
                'by': 'severity',
                'direction': 'descending'
            },
            'pagination': {
                'page': 1,
                'perPage': 2500
            }
        }

        project_request = requests.post(project_request_url, headers={'Content-Type':'application/json', 'API-Key':config['secret-token']}, json=project_request_data)
        project_response_data = json.loads(project_request.text)

    except:
        project_response_data = []
        print('ERROR - GetProjectFindings(): Request Error')

    return project_response_data



def BuildResultAnalytics(results):
    analytics_build = {
        'totals': {
            'High': 0,
            'Medium': 0,
            'Low': 0
        },
        'dynamic': {
            'High': 0,
            'Medium': 0,
            'Low': 0
        },
        'static': {
            'High': 0,
            'Medium': 0,
            'Low': 0
        },
        'component': {
            'High': 0,
            'Medium': 0,
            'Low': 0
        }
    }

    for row in results[1:]:
        analytics_build[row[3]][row[2]] += 1

    analytics_build['totals']['High'] = analytics_build['dynamic']['High'] + analytics_build['static']['High'] + analytics_build['component']['High']
    analytics_build['totals']['Medium'] = analytics_build['dynamic']['Medium'] + analytics_build['static']['Medium'] + analytics_build['component']['Medium']
    analytics_build['totals']['Low'] = analytics_build['dynamic']['Low'] + analytics_build['static']['Low'] + analytics_build['component']['Low']

    analytics = [
        ['Totals'],
        ['', 'High', analytics_build['totals']['High']],
        ['', 'Meduim', analytics_build['totals']['Medium']],
        ['', 'Low', analytics_build['totals']['Low']],
        ['Scan Types'],
        ['', 'Dynamic'],
        ['', '', 'High', analytics_build['dynamic']['High']],
        ['', '', 'Meduim', analytics_build['dynamic']['Medium']],
        ['', '', 'Low', analytics_build['dynamic']['Low']],
        ['', 'Static'],
        ['', '', 'High', analytics_build['static']['High']],
        ['', '', 'Meduim', analytics_build['static']['Medium']],
        ['', '', 'Low', analytics_build['static']['Low']],
        ['', 'Component'],
        ['', '', 'High', analytics_build['component']['High']],
        ['', '', 'Meduim', analytics_build['component']['Medium']],
        ['', '', 'Low', analytics_build['component']['Low']]
    ]

    return analytics



def FormatFindingsForXlsx(data):
    format_data = [[
        'link',
        'id',
        'severity',
        'type',
        'tool',
        'label',
        'firstSeenOn',
        'desc_path'
    ]]

    for row in data:
        format_data.append([
            BuildIssueUrl(row['projectId'], row['id']),
            row['id'],
            row['severity']['name'],
            row['simpleDetectionType'],
            row['results'][0]['tool'],
            row['descriptor']['name'],
            row['firstSeenOn'],
            BuildFindingPathString(row['results'][0]['toolHierarchy'])
        ])

    return format_data



def DefineColorsForXlsx(data):
    column_colors = []

    for row in data:
        if ('High' in row):
            column_colors.append('f54842') # red
        elif ('Medium' in row):
            column_colors.append('f57842') # orange
        elif ('Low' in row):
            column_colors.append('f5d142') # yellow
        else:
            column_colors.append('ffffff') # white

    return column_colors







config = LoadConfigFile()

if (config != False):
    for project in config['project-list']:

        print(project['name'] + ':  Get Findings - Start')
        project_findings = GetProjectFindings(project['id'])
        print(project['name'] + ':  Get Findings - Complete')

        if len(project_findings) != 0 and 'error' not in project_findings:
            print(project['name'] + ':  Format Findings - Start')
            project_findings_flat = FormatFindingsForXlsx(project_findings)
            print(project['name'] + ':  Format Findings - Complete')

            print(project['name'] + ':  Define Colors - Start')
            project_findings_xlsx_colors = DefineColorsForXlsx(project_findings_flat)
            print(project['name'] + ':  Define Colors - Complete')

            print(project['name'] + ':  Analytics - Start')
            project_analytics = BuildResultAnalytics(project_findings_flat)
            print(project['name'] + ':  Analytics - Complete')

            print(project['name'] + ':  Build - Start')
            xm.BuildXlsxFile(project['name'], project_findings_flat, project_findings_xlsx_colors, project_analytics)
            print(project['name'] + ':  Build - Complete')

            print(project['name'] + ':  FINISHED\n')

        else:
            print('ERROR - zero findings or request error')