import configparser
from collections import OrderedDict
import logging
import re

# This module has two glob variables
config_file = ['config.ini',]
config = OrderedDict()


def set_active_config_file(new_config_file):
    """Set the active config
    
    Arguments:
        new_config_file {string} -- Path to a config file
    """
    global config_file
    global config

    config_file[0] = new_config_file
    config.clear()
    config.update(read_configfile(config_file[0]))


def get_active_config_file():
    """Get the current active config file
    
    Returns:
        string -- Return the path to the active config file
    """
    global config_file
    return config_file[0]


def get_config(active_config, section):
    """Return a dictionary of the specified section in given or activate config
    
    Arguments:
        section {string} -- A section in the active config file
    
    Returns:
        OrderedDict -- configuration as dictionary, empty dictionary in case section is not found
    """
    if active_config is None:
        global config
        active_config = config

    if section is None:
        section = 'global'

    try:
        return active_config[section]
    except KeyError:
        logging.warn('Config section %s not found!', section)
        return {}


def read_configfile(config_file, parse_parameters=True):
    """Reads active config file from disk and returns it as dictionary
    """
    #print(f'Reading config file {config_file} ...')
    cfg = OrderedDict()
    try:
        cfg_parser = configparser.ConfigParser(allow_no_value=True)
        cfg_parser.optionxform = str  # Keeps options to be all set to lowercases
        cfg_parser.read_file(open(config_file))

        for section in cfg_parser.sections():
            parameters = dict()
            for option in cfg_parser.options(section):
                try:
                    parameter = cfg_parser.get(section, option)
                    if parse_parameters:
                        parameter = __parse_parameter(parameter)
                    parameters[option] = parameter
                except KeyError:
                    logging.error(format("Exception on config file option [%s]!" % option))
                    parameters[option] = None

            cfg[section] = parameters
    except Exception as e:
        logging.error('Reading the config file produced an error! %s', e)
    return cfg


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
    """Try to detect parameter type
    """
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
    