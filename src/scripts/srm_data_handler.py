import json, requests, math
import modules.module_console as con


def GetProjectIdsAndNames(config):
    try:
        request_url = config['hosts']['srm'] + '/x/projects?expand=false'

        request = requests.get(request_url, headers={'Content-Type':'application/json', 'API-Key':config['secret-token']})
        response_data = json.loads(request.text)

        if ('error' in response_data):
            con.Error('ERROR: GetProjectIdsAndNames() http response')
            response_data = False
        else:
            response_data = response_data

    except Exception as error:
        con.Error(error)
        response_data = False

    return response_data


def GetProjectFindingsCount(config, project_id):
    try:
        project_request_url = config['hosts']['srm'] + '/api/projects/' + project_id + '/findings/count'

        project_request_data = {
            'filter': {
                'severity': ['Critical', 'High', 'Medium', 'Low']
            },
            'sort': {
                'by': 'severity',
                'direction': 'descending'
            },
            'pagination': {
                'page': 0,
                'perPage': 0
            }
        }

        project_request = requests.post(project_request_url, headers={'Content-Type':'application/json', 'API-Key':config['secret-token']}, json=project_request_data)
        project_response_data = json.loads(project_request.text)

        if ('error' in project_response_data):
            con.Error('ERROR: GetProjectFindingsCount() http response')
            project_response_data = False
        else:
            project_response_data = project_response_data['count']

    except Exception as error:
        con.Error(error)
        project_response_data = False

    return project_response_data


def GetProjectFindings(config, project_id):
    project_findings_count = GetProjectFindingsCount(config, project_id)
    project_findings_per_page = 2500
    project_findings_total_pages = math.ceil(project_findings_count / project_findings_per_page)
    project_findings_data = []

    for i in range(project_findings_total_pages):
        try:
            project_request_url = config['hosts']['srm'] + '/api/projects/' + project_id + '/findings/table?expand=results,triage-time'

            project_request_data = {
                'filter': {
                    'severity': ['Critical', 'High', 'Medium', 'Low']
                },
                'sort': {
                    'by': 'severity',
                    'direction': 'descending'
                },
                'pagination': {
                    'page': (i + 1),
                    'perPage': project_findings_per_page
                }
            }

            project_request = requests.post(project_request_url, headers={'Content-Type':'application/json', 'API-Key':config['secret-token']}, json=project_request_data)
            project_response_data = json.loads(project_request.text)

            if ('error' in project_response_data):
                con.Error('ERROR: GetProjectFindings() http response')
                project_findings_data = False
            else:
                project_findings_data += project_response_data

        except Exception as error:
            con.Error(error)
            project_response_data = False

        project_findings_data_filtered = FilterProjectFindings(project_findings_data)
        project_findings_data_filtered = SetProjectNames(config, project_findings_data)

    return project_findings_data_filtered


def FilterProjectFindings(data):
    filtered_data = []
    excluded_status_list = [
        # None,
        'false-positive',
        'fixed',
        'ignored',
        # 'to-be-fixed',
        # 'reopened'
    ]

    for row in data:
        add_row = True

        if row['status'] in excluded_status_list:
            add_row = False

        if add_row == True:
            filtered_data.append(row)

    return filtered_data

def SetProjectNames(config, data):
    id_name_pair = {}

    for row in data:
        if (row['projectId'] not in id_name_pair.keys()):
            id_name_pair[row['projectId']] = ''

    srm_projects_list = GetProjectIdsAndNames(config)

    for project in srm_projects_list:
        if (project['id'] in id_name_pair.keys()):
            id_name_pair[project['id']] = project['name']

    for x in range(len(data)):
        data[x]['projectName'] = id_name_pair[data[x]['projectId']]

    return data