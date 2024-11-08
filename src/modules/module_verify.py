import json, os, subprocess
import module_console as con


def VerifyNetwork():
    connected_ssid = subprocess.check_output("powershell.exe (get-netconnectionProfile).Name", shell=True).strip().split('\\n')[-1]


def PrepareReport(report):
    report = report.replace('__GOOD__', '\33[32mGOOD\33[0m').replace('__BAD__', '\33[101mFAIL\33[0m')
    return report


def VerifyConfigFile(config):
    os.system('')

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

            if (len(config['projects']) == 0):
                issues_found += 1
                config['projects'] = '__BAD__'
            else:
                for i_proj, project in enumerate(config['projects']):
                    if (project['id'] != ''):
                        config['projects'][i_proj]['id'] = '__GOOD__'
                    else:
                        issues_found += 1
                        config['projects'][i_proj]['id'] = '__BAD__'

                    if (project['name'] != ''):
                        config['projects'][i_proj]['name'] = '__GOOD__'
                    else:
                        issues_found += 1
                        config['projects'][i_proj]['name'] = '__BAD__'

                    if (len(project['contacts']) == 0):
                        issues_found += 1
                        config['projects'][i_proj]['contacts'] = '__BAD__'
                    else:
                        for i_cont, contact in enumerate(project['contacts']):
                            if (contact['role'] != ''):
                                config['projects'][i_proj]['contacts'][i_cont]['role'] = '__GOOD__'
                            else:
                                issues_found += 1
                                config['projects'][i_proj]['contacts'][i_cont]['role'] = '__BAD__'

                            if (contact['name'] != ''):
                                config['projects'][i_proj]['contacts'][i_cont]['name'] = '__GOOD__'
                            else:
                                issues_found += 1
                                config['projects'][i_proj]['contacts'][i_cont]['name'] = '__BAD__'

                            if (contact['email'] != ''):
                                config['projects'][i_proj]['contacts'][i_cont]['email'] = '__GOOD__'
                            else:
                                issues_found += 1
                                config['projects'][i_proj]['contacts'][i_cont]['email'] = '__BAD__'


        else:
            issues_found += 1
            print('config file missing')


        if (issues_found != 0):
            print(PrepareReport(json.dumps(config, indent=4)))

        else:
            print(PrepareReport(json.dumps(config, indent=4)))
            con.Pass('\nConfig File Was Verified and Passed')

    except Exception as error:
        con.Error('invalid config format')
