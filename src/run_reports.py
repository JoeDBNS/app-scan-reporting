import json, os
import modules.module_verify as verify
import scripts.report as report
import scripts.analytics as analytics
import modules.module_xlsx_maker as xm
import modules.module_console as con
import modules.module_email as eml



# Load config json from local config.json file
def LoadConfigFile():
    try:
        with open('./src/config/main.json') as file:
            return json.load(file)
    except Exception as error:
        return False


def VerifyToolSetup(config):
    issue_count = 0
    issue_count += verify.VerifyConfigFile(config)
    issue_count += verify.VerifyNetwork(config)

    if (issue_count == 0):
        return True
    else:
        return False


# Required to initialize escape characters in terminal
os.system('')

print('\n\n')

config = LoadConfigFile()

if (config != False):
    con.Pass('Config File Loaded')

    if (VerifyToolSetup(config) == True):

        for project in config['projects']:
            print('\n')
            con.Info(project['name'])

            findings_worksheet = report.BuildReport(config, project['id'])
            con.Info('LOAD:\tBUILD ANALYTICS')
            analytics_worksheet = analytics.BuildAnalytics(findings_worksheet['data'])
            con.Pass('\033[FDONE\tBUILD ANALYTICS')

            wb_content = {
                'name': 'AVR - ' + project['name'],
                'sheets': [
                    analytics_worksheet,
                    findings_worksheet
                ]
            }

            con.Info('LOAD:\tBUILDING XLSX')
            file_path = xm.BuildXlsxFile(wb_content)
            con.Pass('\033[FDONE\tBUILDING XLSX')

            con.Info('LOAD:\tSENDING EMAILS')
            try:
                for contact in project['contacts']:
                    eml.SendEmailWithAttachment(
                        config,
                        recipient=', '.join(contact['emails']),
                        subject=f'AppScan Results: {project['name']}',
                        body='',
                        attachment_path=file_path,
                        attachment_name=project['name'] + '.xlsx'
                    )
                con.Pass('\033[FDONE\tSENDING EMAILS')

            except Exception as error:
                con.Error('\033[FERROR:\tSENDING EMAILS')

    else:
        con.Error('ERROR:\tISSUES WITH TOOL VERIFICATION')

else:
    con.Error('ERROR:\tLOADING CONFIG FILE')