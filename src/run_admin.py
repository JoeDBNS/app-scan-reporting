import json, os, pick
import modules.module_console as con



# Load config json from local config.json file
def LoadConfigFile():
    try:
        with open('./src/config/main.json') as file:
            return json.load(file)
    except Exception as error:
        return False


# Required to initialize escape characters in terminal
os.system('')

print('\n\n')

config = LoadConfigFile()

if (config != False):
    con.Pass('Config File Loaded')

    action_options = ['Build', 'Edit', 'View']
    action_choice, action_choice_index = pick.pick(action_options, '\nDo you want to Build, Edit, or View your config file? ')

    while (action_choice not in action_options):
        print('invalid entry')
        action_choice = input('\n\nDo you want to run [view] or [edit] your config file? ').lower().strip()

    if (action_choice == 'View'):
        print()
        print('smtp:', json.dumps(json.loads(str(config['smtp']).replace('\'', '"')), indent=4))
        print('\nhosts:', json.dumps(json.loads(str(config['hosts']).replace('\'', '"')), indent=4))
        print('\nsecret-token:', '"' + config['secret-token'] + '"')
        print('\nprojects:')

        for project in config['projects']:
            print()
            print('\tid:', '"' + str(project['id']) + '"')
            print('\tname:', '"' + project['name'] + '"')
            print('\treports:')

            for report in project['reports']:
                print('\t\ttype:', '"' + report['type'] + '"')
                print('\t\tcontacts:')

                for contact in report['contacts']:
                    print('\t\t\trole:', '"' + contact['role'] + '"')
                    print('\t\t\tname:', '"' + contact['name'] + '"')
                    print('\t\t\temails:')

                    for email in contact['emails']:
                        print('\t\t\t\t' + '"' + email + '"')

                    print()
                print()

    elif (action_choice == 'Build'):
        print()
        email_sender_name = input('Email Display Name:\t').strip()
        email_sender_email = input('Email Address:\t\t').strip()
        secret_token = input('SRM Secret Token:\t').strip()

        projects_choice = input('\nDo you want to add a project? (y/n) ').lower().strip()
        projects = []

        while (projects_choice == 'y'):
            new_project = {}
            new_project_id = input('Project Id: ').strip()
            new_project_name = input('Project Name: ').strip()

            contacts_choice = 'y'
            contacts = []

            while (contacts_choice == 'y'):
                new_contact = {}
                new_contact_role = input('Contact Role: ').strip()
                new_contact_name = input('Contact Name: ').strip()

                emails_choice = 'y'
                emails = []

                while (emails_choice == 'y'):
                    new_email = input('Email Address: ').strip()

                    emails.append(new_email)
                    emails_choice = input('\nDo you want to add another email? (y/n) ').lower().strip()

                contacts.append(new_contact)
                contacts_choice = input('\nDo you want to add another contact? (y/n) ').lower().strip()

            projects.append(new_project)
            projects_choice = input('\nDo you want to add another project? (y/n) ').lower().strip()

    elif (action_choice == 'Edit'):
        print()
        print('edit')

else:
    con.Error('ERROR:\tLOADING CONFIG FILE')