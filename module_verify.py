import json, os
import module_console as con


# Load config json from local config.json file
def LoadConfigFile():
    try:
        with open('./config/main.json') as file:
            return json.load(file)
    except Exception as error:
        return False



def PrepareReport(report):
    report = report.replace('__GOOD__', '\33[32mGOOD\33[0m').replace('__BAD__', '\33[101mFAIL\33[0m')
    return report





os.system('')

config = LoadConfigFile()

issues_found = 0

try:
    if (config != False):
        if (config['smtp']['host'] != ''):
            config['smtp']['host'] = '__GOOD__'
        else:
            issues_found += 1
            config['smtp']['host'] = '__BAD__'

        if (config['smtp']['port'] != 0):
            config['smtp']['port'] = '__GOOD__'
        else:
            issues_found += 1
            config['smtp']['port'] = '__BAD__'

        if (config['smtp']['sender']['name'] != ''):
            config['smtp']['sender']['name'] = '__GOOD__'
        else:
            issues_found += 1
            config['smtp']['sender']['name'] = '__BAD__'

        if (config['smtp']['sender']['email'] != ''):
            config['smtp']['sender']['email'] = '__GOOD__'
        else:
            issues_found += 1
            config['smtp']['sender']['email'] = '__BAD__'

        if (config['hosts']['srm'] != ''):
            config['hosts']['srm'] = '__GOOD__'
        else:
            issues_found += 1
            config['hosts']['srm'] = '__BAD__'

        if (config['secret-token'] != ''):
            config['secret-token'] = '__GOOD__'
        else:
            issues_found += 1
            config['secret-token'] = '__BAD__'

        for i, project in enumerate(config['projects']):
            if (project['id'] != ''):
                config['projects'][i]['id'] = '__GOOD__'
            else:
                issues_found += 1
                config['projects'][i]['id'] = '__BAD__'

            if (project['name'] != ''):
                config['projects'][i]['name'] = '__GOOD__'
            else:
                issues_found += 1
                config['projects'][i]['name'] = '__BAD__'

            for i, contact in enumerate(project['contacts']):
                if (project['id'] != ''):
                    config['projects'][i]['id'] = '__GOOD__'
                else:
                    issues_found += 1
                    config['projects'][i]['id'] = '__BAD__'

                if (project['name'] != ''):
                    config['projects'][i]['name'] = '__GOOD__'
                else:
                    issues_found += 1
                    config['projects'][i]['name'] = '__BAD__'


    else:
        issues_found += 1
        print('config file missing')


    if (issues_found != 0):
        print(PrepareReport(json.dumps(config, indent=4)))

    else:
        print(PrepareReport(json.dumps(config, indent=4)))
        con.Pass('Config File Was Verified and Passed')

except Exception as error:
    con.Error('invalid config format')



# - has data for all hosts
# - has a secret token
# - has at least 1 project
# - every project has an id and a name
# - every project contact has an email


# PASS
# '\33[32mGOOD\33[0m'

# FAIL
# '\33[101mFAIL\33[0m'