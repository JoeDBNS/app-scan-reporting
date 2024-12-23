import json, requests


def GetProjectFindings(config, project_id):
    try:
        project_request_url = config['hosts']['srm'] + '/api/projects/' + str(project_id) + '/findings/table?expand=results,triage-time'

        project_request_data = {
            'filter': {
                'severity': ['Critical', 'High', 'Medium', 'Low']
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

    return FilterProjectFindings(project_response_data)


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