import configfy
from configfy import configfy as cfy 

@cfy
def hello(name, another_name='Pedro'):
    """Some print statement 
    """
    print('Hello %s, I am %s!' % (name, another_name))


@cfy(section='greetings_section')
def greetings(name, language='english'):
    """Give a nice greeting ...
    """
    if language == 'english':
        print('Hello %s! How are you doing?' % (name))
    elif language == 'spanish':
        print('Hola %s! Que tal?' % (name))
    elif language == 'german':
        print('Hallo %s! Wie gehts?' % (name))
    elif language == 'serbian':
        print('Zdravo %s! Kako si?' % (name))
    else:
        print('!nuqneH %s!' % (name))


@cfy(config='yet_another_config.ini')
def goodby(msg='Goodby!'):
    print(msg)

print('# Use default config.ini file (missing greetings section)...')
hello('Bob')
greetings('Tom')
goodby()

print('\n# Changing config to "another_config.ini" ...')
configfy.set_active_config_file('another_config.ini')
hello('Bob')
greetings('Tom')
goodby()

print('\n# Specifying kwargs, overwriting config settings...')
hello('Bob', another_name='Alfredo')
greetings('Tom', language='serbian')
goodby(msg='That\'s all Folks!')
