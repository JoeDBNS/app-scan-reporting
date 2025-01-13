import json, subprocess, copy
import modules.module_console as con


def VerifyNetwork(config):
    issues_found = 0

    connected_network = str(subprocess.check_output("powershell.exe (get-netconnectionProfile).Name", shell=True).strip()).replace('b\'', '').replace('\'', '').replace('\\r', '').split("\\n")

    if (config['hosts']['internal-network'] not in connected_network):
        con.Error('\nNOT ON SOM NETWORK: "' + str(connected_network) + '"')
        issues_found += 1

    return issues_found


def PrepareReport(report):
    report = report.replace('__GOOD__', '\33[32mGOOD\33[0m').replace('__BAD__', '\33[101mFAIL\33[0m')
    return report


def VerifyConfigFile(config):
    config_report = copy.deepcopy(config)
    issues_found = 0

    try:
        if (config_report != False):
            if (config_report['smtp']['host'] != ''):
                config_report['smtp']['host'] = '__GOOD__'
            else:
                issues_found += 1
                config_report['smtp']['host'] = '__BAD__'

            if (config_report['smtp']['port'] != 0):
                config_report['smtp']['port'] = '__GOOD__'
            else:
                issues_found += 1
                config_report['smtp']['port'] = '__BAD__'

            if (config_report['smtp']['sender']['name'] != ''):
                config_report['smtp']['sender']['name'] = '__GOOD__'
            else:
                issues_found += 1
                config_report['smtp']['sender']['name'] = '__BAD__'

            if (config_report['smtp']['sender']['email'] != ''):
                config_report['smtp']['sender']['email'] = '__GOOD__'
            else:
                issues_found += 1
                config_report['smtp']['sender']['email'] = '__BAD__'

            if (config_report['hosts']['srm'] != ''):
                config_report['hosts']['srm'] = '__GOOD__'
            else:
                issues_found += 1
                config_report['hosts']['srm'] = '__BAD__'

            if (config_report['hosts']['internal-network'] != ''):
                config_report['hosts']['internal-network'] = '__GOOD__'
            else:
                issues_found += 1
                config_report['hosts']['internal-network'] = '__BAD__'

            if (config_report['secret-token'] != ''):
                config_report['secret-token'] = '__GOOD__'
            else:
                issues_found += 1
                config_report['secret-token'] = '__BAD__'

            if (len(config_report['projects']) == 0):
                issues_found += 1
                config_report['projects'] = '__BAD__'
            else:
                for i_proj, project in enumerate(config_report['projects']):
                    if (project['id'] != ''):
                        config_report['projects'][i_proj]['id'] = '__GOOD__'
                    else:
                        issues_found += 1
                        config_report['projects'][i_proj]['id'] = '__BAD__'

                    if (project['name'] != ''):
                        config_report['projects'][i_proj]['name'] = '__GOOD__'
                    else:
                        issues_found += 1
                        config_report['projects'][i_proj]['name'] = '__BAD__'

                    if (len(project['reports']) == 0):
                        issues_found += 1
                        config_report['projects'][i_proj]['reports'] = '__BAD__'
                    else:
                        for i_rport, report in enumerate(project['reports']):
                            if (len(report['contacts']) == 0):
                                issues_found += 1
                                config_report['projects'][i_proj]['reports'][i_rport]['contacts'] = '__BAD__'
                            else:
                                for i_cont, contact in enumerate(report['contacts']):
                                    if (contact['role'] != ''):
                                        config_report['projects'][i_proj]['reports'][i_rport]['contacts'][i_cont]['role'] = '__GOOD__'
                                    else:
                                        issues_found += 1
                                        config_report['projects'][i_proj]['reports'][i_rport]['contacts'][i_cont]['role'] = '__BAD__'

                                    if (contact['name'] != ''):
                                        config_report['projects'][i_proj]['reports'][i_rport]['contacts'][i_cont]['name'] = '__GOOD__'
                                    else:
                                        issues_found += 1
                                        config_report['projects'][i_proj]['reports'][i_rport]['contacts'][i_cont]['name'] = '__BAD__'

                                    if (len(contact['emails']) == 0):
                                        issues_found += 1
                                        config_report['projects'][i_proj]['reports'][i_rport]['contacts'][i_cont]['emails'] = '__BAD__'
                                    else:
                                        config_report['projects'][i_proj]['reports'][i_rport]['contacts'][i_cont]['emails'] = '__GOOD__'

                                    if (contact['secure-delivery'] != ''):
                                        config_report['projects'][i_proj]['reports'][i_rport]['contacts'][i_cont]['secure-delivery'] = '__GOOD__'
                                    else:
                                        issues_found += 1
                                        config_report['projects'][i_proj]['reports'][i_rport]['contacts'][i_cont]['secure-delivery'] = '__BAD__'

                                    if (contact['secure-delivery']['7zip'] != ''):
                                        config_report['projects'][i_proj]['reports'][i_rport]['contacts'][i_cont]['secure-delivery']['7zip'] = '__GOOD__'
                                    else:
                                        issues_found += 1
                                        config_report['projects'][i_proj]['reports'][i_rport]['contacts'][i_cont]['secure-delivery']['7zip'] = '__BAD__'

                                    if (contact['secure-delivery']['7zip'] != True):
                                        if (contact['secure-delivery']['password'] != ''):
                                            config_report['projects'][i_proj]['reports'][i_rport]['contacts'][i_cont]['secure-delivery']['password'] = '__GOOD__'
                                        else:
                                            issues_found += 1
                                            config_report['projects'][i_proj]['reports'][i_rport]['contacts'][i_cont]['secure-delivery']['password'] = '__BAD__'


        else:
            issues_found += 1
            print('config file missing')


        if (issues_found != 0):
            print('\n', PrepareReport(json.dumps(config_report, indent=4)))

        else:
            print('\n', PrepareReport(json.dumps(config_report, indent=4)))
            con.Pass('\nConfig File Was Verified and Passed')

    except Exception as error:
        con.Error('invalid config format')
        issues_found += 1


    return issues_found
