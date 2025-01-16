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

else:
    con.Error('ERROR:\tLOADING CONFIG FILE')