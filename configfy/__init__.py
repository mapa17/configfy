from configfy.decorator import configfy_func
from configfy.decorator import configfy_class
from configfy.configfile import set_active_config_file, get_active_config_file, read_config, get_config

# On import read config
read_config()