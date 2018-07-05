import configparser
from collections import OrderedDict
import logging
import re

# This module has two glob variables
config_file = ['config.ini',]
config = OrderedDict()


def set_active_config_file(new_config_file):
    global config_file
    config_file[0] = new_config_file
    read_config()


def get_active_config_file():
    global config_file
    return config_file[0]


def get_config(section):
    global config
    if section is None:
        section = 'global'
    try:
        return config[section]
    except KeyError:
        logging.warn(f'Config section {section} not found!')
        return {}


def read_config():
    """Reads active config file from disk
    """
    active_config_file = get_active_config_file()
    print(f'Reading config file {active_config_file} ...')
    cfg = OrderedDict()
    try:
        cfg_parser = configparser.ConfigParser(allow_no_value=True)
        cfg_parser.optionxform = str  # Keeps options to be all set to lowercases
        cfg_parser.read_file(open(active_config_file))

        for section in cfg_parser.sections():
            parameters = dict()
            for option in cfg_parser.options(section):
                try:
                    parameter = cfg_parser.get(section, option)
                    parameters[option] = __parse_parameter(parameter)
                except KeyError:
                    logging.error(format("Exception on config file option [%s]!" % option))
                    parameters[option] = None

            cfg[section] = parameters
    except Exception as e:
        logging.error('Reading the config file produced an error! %s', e)

    global config
    config.update(cfg)


def parser_list(string):
    """Helper function that parsers a string containing a list
    
    Arguments:
        string {str} -- Paramter string
    """
    # Remove [] and whitespaces
    cleaned = re.sub('[\[\]\s]', '', string)

    # Split
    parts = cleaned.split(',')

    # Use the default parser
    converted = [__parse_parameter(x) for x in parts]

    return converted


def __parse_parameter(parameter):
    result = None

    if parameter == '':
        result = None
    elif parameter.lower() == 'none':
        result = None
    elif parameter.lower() == 'true':
        result = True
    elif parameter.lower() == 'false':
        result = False
    elif parameter.lstrip('-+').isnumeric():
        try:
            result = float(parameter)
        except ValueError:
            pass
    else:
        result = str(parameter)
    return result 


def readconfig(fileName='config.ini', tagName=None):
    """
    Read python config file using ConfigParser
    Will read all options under the region "tagName" and if possible convert a
    value into float.
    """



    