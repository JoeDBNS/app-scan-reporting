import json
import requests



try:
    with open('./config/main.json') as file:
        config = json.load(file)
except:
    config = False
    print('ERROR: File not found (./config/main.json)')



if (config != False):
    try:
        request_url = 'https://asoc.state.mi.us/srm/api/projects/' + config['project-id'] + '/findings/count'
        request = requests.get(request_url, headers={'Content-Type':'application/json', 'API-Key':config['secret-token']})
    except:
        request = False
        print('ERROR: Must be on SOM network')


    print(request.text)

