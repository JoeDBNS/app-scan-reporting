import json
import requests



try:
    with open('./config/main.json') as file:
      config = json.load(file)
except:
    config = False
    print("File not found (./config/main.json)")



if (config != False):
    request = requests.get("https://asoc.state.mi.us/srm/api/projects/1037/findings/count", headers={"Content-Type":"application/json", "API-Key":config['secret-token']})

    print(request.text)

