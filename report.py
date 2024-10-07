import json, requests, os
import xlsx_maker as xm
import email as eml
import console as con


# Load config json from local config.json file
def LoadConfigFile():
    try:
        with open('./config/main.json') as file:
            return json.load(file)
    except:
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

        if ('error' not in project_response_data):
            project_response_data = False

    except:
        project_response_data = False

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






print('\n\n')

os.system('')

config = LoadConfigFile()

if (config != False):
    con.Pass('Config File Loaded')

    for project in config['project-list']:
        print('\n\n')
        con.Info(project['name'])

        con.Info('LOAD:\tGET FINDINGS')
        project_findings = GetProjectFindings(project['id'])

        if (project_findings != False):
            con.Pass('\033[FDONE\tGET FINDINGS')

            if len(project_findings) != 0:
                con.Info('LOAD:\tFORMAT FINDINGS')
                project_findings_flat = FormatFindingsForXlsx(project_findings)
                con.Pass('\033[FDONE\tFORMAT FINDINGS')

                con.Info('LOAD:\tDEFINE COLORS')
                project_findings_xlsx_colors = DefineColorsForXlsx(project_findings_flat)
                con.Pass('\033[FDONE\tDEFINE COLORS')

                con.Info('LOAD:\tBUILD ANALYTICS')
                project_analytics = BuildResultAnalytics(project_findings_flat)
                con.Pass('\033[FDONE\tBUILD ANALYTICS')

                con.Info('LOAD:\tBUILD FILE')
                file_path = xm.BuildXlsxFile(project['name'], project_findings_flat, project_findings_xlsx_colors, project_analytics)
                con.Pass('\033[FDONE\tBUILD FILE')

                con.Info('LOAD:\tSENDING EMAILS')
                try:
                    for contact in project['contacts']:
                        eml.SendEmailWithAttachment(
                            recipient=contact['email'],
                            subject=f'AppScan Results: {project['name']}',
                            body='',
                            attachment_path=file_path,
                            attachment_name=project['name']
                        )
                    con.Pass('\033[FDONE\tSENDING EMAILS')

                except:
                    con.Error('\033[FERROR:\tSENDING EMAILS')

            else:
                con.Error('\033[FERROR:\tZERO FINDINGS')

        else:
            con.Error('\033[FERROR:\tGET FINDINGS')
else:
    con.Error('\033[FERROR:\tLOADING CONFIG FILE')