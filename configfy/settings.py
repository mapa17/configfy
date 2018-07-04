config_file = ['config.ini',]

def set_active_config(new_config_file):
    global config_file
    config_file[0] = new_config_file

def get_active_config():
    global config_file
    return config_file[0]
    