# Setup logging to console on warnings and errors
import logging
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.WARN)
formatter = logging.Formatter('# %(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

from configfy.decorator import configfy
from configfy.configfile import set_active_config_file, get_active_config_file, read_configfile, get_config

# On import read config
set_active_config_file(get_active_config_file())
