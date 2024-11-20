import json, os, py7zr
import modules.module_verify as verify
import scripts.srm_data_handler as srm_data_handler
import scripts.report_builder as report_builder
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

            wb_content = {
                'name': 'AVR - ' + project['name'],
                'sheets': []
            }

            con.Info('\tLOAD:\tGET FINDINGS')
            project_findings = srm_data_handler.GetProjectFindings(config, project['id'])

            if (project_findings != False):
                con.Pass('\033[F\tDONE\tGET FINDINGS')

                if len(project_findings) != 0:
                    report_count = 0
                    for report in project['reports']:
                        if (report_count > 0):
                            print('')

                        con.Info('\tTYPE:\t' + report['type'])

                        if report['type'] == 'development':
                            ws_list_build = ['analytics', 'findings_detailed']
                            wb_content['name'] = 'AVR - ' + project['name'] + ' - detailed'
                            wb_content['sheets'] = report_builder.BuildReports(config, ws_list_build, project_findings)

                        elif report['type'] == 'executive':
                            ws_list_build = ['charts', 'findings_simple']
                            wb_content['name'] = 'AVR - ' + project['name'] + ' - executive'
                            wb_content['sheets'] = report_builder.BuildReports(config, ws_list_build, project_findings)

                        else:
                            con.Error('\tERROR:\tINVALID REPORT TYPE - ' + report['type'])

                        if (len(wb_content['sheets']) > 0):
                            con.Info('\t\tLOAD:\tBUILDING XLSX')
                            file_path = xm.BuildXlsxFile(wb_content)
                            con.Pass('\033[F\t\tDONE\tBUILDING XLSX')

                            con.Info('\t\tLOAD:\tSENDING EMAILS')
                            try:
                                attachment_base_name = project['name'] + ' - ' + report['type']
                                attachment_type = ''

                                for contact in report['contacts']:
                                    if (contact['secure-delivery']['7zip'] == True):
                                        try:
                                            with py7zr.SevenZipFile(file_path.replace('.xlsx', '.7z'), 'w', password=contact['secure-delivery']['password']) as archive:
                                                archive.writeall(file_path, attachment_base_name +'.xlsx')
                                            attachment_type = '.7z'
                                        except Exception as error:
                                            con.Error('\t\tERROR:\t7zip FILES')
                                    else:
                                        attachment_type = '.xlsx'

                                    eml.SendEmailWithAttachment(
                                        config,
                                        recipient=', '.join(contact['emails']),
                                        subject=f'AppScan Results: {project['name']}',
                                        body=f'AppScan Report for:\n{project['name']}\n\nReport Type:\n{report['type']}\n\nReport Target:\n{contact['role']}',
                                        attachment_path=file_path,
                                        attachment_name=attachment_base_name + attachment_type
                                    )
                                con.Pass('\033[F\t\tDONE\tSENDING EMAILS')

                            except Exception as error:
                                con.Error('\t\tERROR:\tSENDING EMAILS')

                    report_count += 1

            else:
                con.Error('\033[F\tERROR:\tGET FINDINGS')

    else:
        con.Error('ERROR:\tISSUES WITH TOOL VERIFICATION')

else:
    con.Error('ERROR:\tLOADING CONFIG FILE')