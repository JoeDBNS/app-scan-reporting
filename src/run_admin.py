import json, os
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

    action_options = ['build', 'edit', 'view']
    action_choice = input('\nDo you want to run [build], [edit], or [view] your config file? ').lower().strip()

    while (action_choice not in action_options):
        print('invalid entry')
        action_choice = input('\n\nDo you want to run [view] or [edit] your config file? ').lower().strip()

    if (action_choice == 'view'):
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

    elif (action_choice == 'build'):
        print()
        email_sender_name = input('Email Display Name: ').strip()
        email_sender_email = input('Email Address: ').strip()
        secret_token = input('SRM Secret Token: ').strip()

    elif (action_choice == 'edit'):
        print()
        print('edit')

else:
    con.Error('ERROR:\tLOADING CONFIG FILE')