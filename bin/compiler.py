import configparser
import os
from pprint import pprint
from pathlib import Path
import json
from shutil import copyfile

PATH_SECTION = 'Paths'

directory = os.getcwd().split('/').pop()

if "bin" == directory:
    print("Please run this command from the project directory")
    exit()

config = Path('config.ini')
if not config.is_file():
    print("File config.ini not found, you might want to run make setup command")
    exit()


# Will create the path for the new config file and remove it if it already exists
def init_file(config_path):
    config_file = Path(config_path)
    if not config_file.is_file():
        print('Config file %s does not exist, skipping configuration' % config_path)
        return False

    new_config_path = config_path.replace('config', 'config.compiled')
    if os.path.exists(new_config_path):
        os.remove(new_config_path)
        return True

    dirname = os.path.dirname(new_config_path)
    if not os.path.exists(dirname):
        os.mkdir(os.path.dirname(new_config_path))

    return True


def json_handler(config_value):
    data = []
    config_value = json.loads(config_value)
    for config_key in config_value:
        data.append('"%s"="%s"' % (config_key, config_value[config_key]))

    return "\n".join(data)


def fill_file(config_path, config_key, config_value):
    new_config_path = config_path.replace('config', 'config.compiled')

    f_in = open(config_path, "rt")
    f_out = open(new_config_path, "wt")
    print(config_key, config_value)

    for line in f_in:
        print(line.replace('%%%%%s%%%%' % config_key, config_value))
        f_out.write(line.replace('%%%%%s%%%%' % config_key, config_value))

    f_in.close()
    f_out.close()


config = configparser.ConfigParser()
config.read('config.ini')

for section in config.sections():
    if PATH_SECTION == section:
        continue

    path = config.get(PATH_SECTION, section)
    path = 'config/%s/%s.conf' % (path, section)
    if not init_file(path):
        continue

    for key in config[section]:
        key_type = key.split('%').pop()
        value = config.get(section, key)
        if 'json' == key_type:
            value = json_handler(value)
            key = key.replace('%json', '')

        fill_file(path, key, value)
