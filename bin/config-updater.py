import configparser
import os
from collections import OrderedDict
from pathlib import Path

PATH_SECTION = 'Paths'
FILE_SECTION = 'ConfigFiles'

directory = os.getcwd().split('/').pop()

if "bin" == directory:
    print("Please run this command from the project directory")
    exit()

config_dist = Path('config.ini.dist')
config = Path('config.ini')
if not config.is_file():
    print("File config.ini not found, you might want to run make setup command")
    exit()


class Parser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr


config = Parser()
config.read('config.ini')

config_dist = Parser()
config_dist.read('config.ini.dist')

config_sections = config.__dict__['_sections'].copy()
config_dist_sections = config_dist.__dict__['_sections'].copy()


def merge_dicts(config_dist_dict, config_dict):
    final_dict = OrderedDict()
    for key, item in config_dist_dict.items():
        final_dict[key] = item
        for item_key, item_value in item.items():
            if key in config_dict and item_key in config_dict[key]:
                final_dict[key][item_key] = config_dict[key][item_key]

    return final_dict


final = merge_dicts(config_dist_sections, config_sections)

config_final = Parser()
config_final.read_dict(final)

with open('config.ini', 'w') as configfile:
    config_final.write(configfile)
