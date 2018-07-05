import configfy
from configfy import configfy as cfy
from pudb import set_trace as st

@cfy
def hello(name, another_name='Pedro'):
    """Some print statement 
    """
    print(f'Hello {name}, I am {another_name}!')


@cfy(section='greetings_section')
def greetings(name, language='english'):
    """Give a nice greeting ...
    """
    if language == 'english':
        print(f'Hello {name}! How are you doing?')
    elif language == 'spanish':
        print(f'Hola {name}! Que tal?')
    elif language == 'german':
        print(f'Hallo {name}! Wie gehts?')
    elif language == 'serbian':
        print(f'Zdravo {name}! Kako si?')
    else:
        print(f'!nuqneH {name}!')


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


import time
import timeit
import numpy as np

def do_stuff(kw_arg=13):
    time.sleep(10.0/1000.0)
    return np.random.random()*kw_arg

@cfy(config='yet_another_config.ini')
def do_stuff_with_configfy(kw_arg=13):
    time.sleep(10.0/1000.0)
    return np.random.random()*kw_arg

N = 1000
print('\nComparing performance ... this can take a while.')
nativ = timeit.timeit('do_stuff()', number=N, globals=globals())
withconfigfy = timeit.timeit('do_stuff_with_configfy()', number=N, globals=globals())

print(f'native: {nativ:2.3f} sec\nconfigfy {withconfigfy:2.3f} sec')
print(f'configfy added {(withconfigfy-nativ)/N} sec to the function call!')
