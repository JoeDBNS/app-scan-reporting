import json, os, py7zr
from yaspin import yaspin
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
    # issue_count += verify.VerifyConfigFile(config)
    issue_count += verify.VerifyNetwork(config)

    if (issue_count == 0):
        return True
    else:
        return False


# Required to initialize escape characters in terminal
os.system('')

print("""
 _____                                                                  _____
( ___ )----------------------------------------------------------------( ___ )
 |   |                                                                  |   |
 |   |      _____          _____         _____           _____          |   |
 |   |     |   __|        |  _  |       | __  |         |   __|         |   |
 |   |     |   __|        |     |       |    -|         |__   |         |   |
 |   |     |_____|xtended |__|__|ppScan |__|__|eporting |_____|uite     |   |
 |___|                                                                  |___|
(_____)----------------------------------------------------------------(_____)
                      ___                   _
                     | _ \\___ _ __  ___ _ _| |_ ___
                     |   / -_) '_ \\/ _ \\ '_|  _(_-<
                     |_|_\\___| .__/\\___/_|  \\__/__/
                             |_|

""")

config = LoadConfigFile()

if (config != False):
    con.Pass('Config File Loaded')

    if (VerifyToolSetup(config) == True):

        for project in config['projects']:
            print('\n')
            con.Info(project['name'])

            wb_content = {
                'name': 'EARS - ' + project['name'],
                'sheets': []
            }

            con.Info('\tLOAD:\tGET FINDINGS')

            with yaspin(text="\tLoading..."):
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
                            wb_content['name'] = 'EARS - ' + project['name'] + ' - detailed'
                            wb_content['sheets'] = report_builder.BuildReports(config, ws_list_build, project_findings)

                        elif report['type'] == 'executive':
                            ws_list_build = ['charts', 'findings_simple']
                            wb_content['name'] = 'EARS - ' + project['name'] + ' - executive'
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
                                                archive.writeall(file_path, attachment_base_name + '.xlsx')
                                            file_path = file_path.replace('.xlsx', '.7z')
                                            attachment_type = '.7z'
                                        except Exception as error:
                                            con.Error('\t\tERROR:\t7zip FILES')
                                    else:
                                        attachment_type = '.xlsx'

                                    eml.SendEmailWithAttachment(
                                        config,
                                        recipients=contact['emails'],
                                        subject=f'Extended Appscan Reporting Suite: {project['name']}',
                                        body=f"""
                                        <html>
                                            <body style="background-color:rgb(30, 30, 30);">
                                                <h1 style="font-size:22px;color:#33ff67;margin-bottom:8px;">
                                                    Extended AppScan Reporting Suite
                                                </h1>

                                                <p style="color:white;">
                                                    <span style="font-size:14px;">AppScan Report for:</span>
                                                    <br>
                                                    <span style="font-weight:bold;">{project['name']}</span>
                                                </p>
                                                <p style="color:white;">
                                                    <span style="font-size:14px;">Report Type:</span>
                                                    <br>
                                                    <span style="font-weight:bold;">{report['type']}</span>
                                                </p>
                                                <p style="color:white;">
                                                    <span style="font-size:14px;">Report Target:</span>
                                                    <br>
                                                    <span style="font-weight:bold;">{contact['role']}</span>
                                                </p>
                                                <br>
                                                <p>
                                                    <span style="font-size:20px;color:red;">⁉️</span><br>
                                                    <span style="font-size:40px;">🖥️</span><br>
                                                    <span style="font-size:32px;">⌨️</span><span style="font-size:20px;">🖱️</span>
                                                </p>
                                            </body>
                                        </html>
                                        """,
                                        attachment_path=file_path,
                                        attachment_name=attachment_base_name + attachment_type
                                    )
                                con.Pass('\033[F\t\tDONE\tSENDING EMAILS')

                            except Exception as error:
                                con.Error('\t\tERROR:\tSENDING EMAILS\n' + str(error))

                    report_count += 1

            else:
                con.Error('\033[F\tERROR:\tGET FINDINGS')

    else:
        con.Error('ERROR:\tISSUES WITH TOOL VERIFICATION')

else:
    con.Error('ERROR:\tLOADING CONFIG FILE')