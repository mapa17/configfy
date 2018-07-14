from configfy.decorator import configfy
from configfy.configfile import set_active_config_file, get_active_config_file, read_configfile, get_config

# On import read config
set_active_config_file(get_active_config_file())
