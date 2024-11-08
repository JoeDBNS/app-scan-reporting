import json, requests
import modules.module_console as con


# Build URL string for specific SRM finding/result/issue
def BuildIssueUrl(config, project_id, issue_id):
    return config['hosts']['srm'] + '/projects/' + str(project_id) + '/findings/' + str(issue_id)



# Build string from issue source path array list
def BuildFindingPathString(path):
    path_as_string = path[0]

    for item in path[1:]:
        path_as_string += ' - ' + item

    return path_as_string



def GetProjectFindings(config, project_id):
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

        if ('error' in project_response_data):
            project_response_data = False

    except Exception as error:
        project_response_data = False

    return project_response_data



# Format field content and flatten data for xlsx
def FormatFindings(config, data):
    format_data = []

    for row in data:
        format_data.append([
            BuildIssueUrl(config, row['projectId'], row['id']),
            row['id'],
            row['severity']['name'],
            row['simpleDetectionType'],
            row['results'][0]['tool'],
            row['descriptor']['name'],
            row['firstSeenOn'],
            BuildFindingPathString(row['results'][0]['toolHierarchy'])
        ])

    return format_data



def BuildReport(config, project_id):
    con.Info('LOAD:\tGET FINDINGS')
    project_findings = GetProjectFindings(config, project_id)

    if (project_findings != False):
        con.Pass('\033[FDONE\tGET FINDINGS')

        if len(project_findings) != 0:
            con.Info('LOAD:\tFORMAT FINDINGS')
            project_findings_flat = FormatFindings(config, project_findings)
            con.Pass('\033[FDONE\tFORMAT FINDINGS')

            con.Info('LOAD:\tBUILD WORKSHEET')
            ws_content = {
                'name': 'Findings',
                'config': {
                    'general': {
                        'add_headers': True
                    },
                    'columns': [
                        {
                            'label': 'link',
                            'size': 30,
                            'filter': False,
                            'is_link': True
                        },
                        {
                            'label': 'id',
                            'size': 0,
                            'filter': False,
                            'is_link': False
                        },
                        {
                            'label': 'severity',
                            'size': 0,
                            'filter': False,
                            'is_link': False
                        },
                        {
                            'label': 'type',
                            'size': 0,
                            'filter': False,
                            'is_link': False
                        },
                        {
                            'label': 'tool',
                            'size': 0,
                            'filter': False,
                            'is_link': False
                        },
                        {
                            'label': 'label',
                            'size': 0,
                            'filter': False,
                            'is_link': False
                        },
                        {
                            'label': 'firstSeenOn',
                            'size': 0,
                            'filter': False,
                            'is_link': False
                        },
                        {
                            'label': 'desc_path',
                            'size': 0,
                            'filter': False,
                            'is_link': False
                        }
                    ],
                    'rows': {
                        'colors': []
                    }
                },
                'data': project_findings_flat
            }

            con.Pass('\033[FDONE\tBUILD WORKSHEET')

            con.Info('LOAD:\tDEFINE COLORS')

            # Color headers row gray
            ws_content['config']['rows']['colors'].append(
                {
                    'row_num': 0,
                    'color_hex': 'd4d4d4'
                }
            )
            # Color data row based on severity
            for i, finding in enumerate(ws_content['data'], start = 1):
                set_color = 'ffffff' # white

                if (finding[2] == 'High'):
                    set_color = 'f54842' # red
                elif (finding[2] == 'Medium'):
                    set_color = 'f57842' # orange
                elif (finding[2] == 'Low'):
                    set_color = 'f5d142' # yellow

                ws_content['config']['rows']['colors'].append(
                    {
                        'row_num': i,
                        'color_hex': set_color
                    }
                )

            con.Pass('\033[FDONE\tDEFINE COLORS')

            return ws_content

        else:
            con.Error('\033[FERROR:\tZERO FINDINGS')

    else:
        con.Error('\033[FERROR:\tGET FINDINGS')