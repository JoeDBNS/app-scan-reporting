import json, requests


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