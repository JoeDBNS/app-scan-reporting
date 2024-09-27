import json
import requests



def LoadConfigFile():
    try:
        with open('./config/main.json') as file:
            return json.load(file)
    except:
        print('ERROR - LoadConfigFile()')
        return False



def BuildIssueUrl(project_id, issue_id):
    return config['hosts']['srm'] + '/projects/' + str(project_id) + '/findings/' + str(issue_id)



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
    analytics = {

    }

    return analytics







config = LoadConfigFile()

if (config != False):
    for project in config['project-list']:

        project_findings = GetProjectFindings(project['id'])

        for item in project_findings:
            print(BuildIssueUrl(project['id'], item['id']))
            # print(item["id"], '-', item["simpleDetectionType"])

        print(project['name'], len(project_findings))
        print('\n\n')