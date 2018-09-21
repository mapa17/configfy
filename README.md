# Configfy
Decorator library to expose keyword arguments through config files

Configfy is a prototyping library that enables fast exposure of function parameters to the user in order modify program behavior without having to handle argument parsing or control the flow of config options through your program. It is implemented as a decorator library that makes use of the python configparser module.

It can be used to quick and dirty add new arguments to an function,
or substitute the complete configuration management for an application.

Hostet on [github](https://github.com/mapa17/configfy)

# Installation
Configfy is best installed using pip

```bash
    pip install configfy
```

# Simple example

Define a function that makes use of keyword arguments, and overwrites the default
keyword argument with a config file setting.

```python
import configfy
from configfy import configfy as cfy 

@cfy
def hello(name, another_name='Pedro'):
    """Be nice and say hello 
    """
    print(f'Hello {name}, I am {another_name}!')

hello('Bob')
```

With a config.ini containing

```ini
[global]
another_name = 'Suzan Flusan'
```

produces

```bash
Hello Bob, I am Suzan Flusan!
```

Note: Be aware that the library expects the presence of a config file (./configfy.ini) containing at least the empty section [global].

# Advanced Example
Show how to specify sections to use in config files and how the config file can be changed during runtime, or specified in the decorator.

> From docs/example.py
```python
import configfy
from configfy import configfy as cfy 

@cfy
def hello(name, another_name='Pedro'):
    """Be nice and say hello 
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


print('# Use default configfy.ini file (missing greetings section)...')
print('# Current config: %s' % configfy.configfile.config)
hello('Bob')
greetings('Tom')
goodby()


print('\n# Changing config to "another_config.ini" ...')
configfy.set_active_config_file('another_config.ini')
print('After setting new config file, current config: %s' % configfy.configfile.config)
hello('Bob')
greetings('Tom')
goodby()


print('\n# Specifying kwargs, overwriting config settings...')
hello('Bob', another_name='Alfredo')
greetings('Tom', language='serbian')
goodby(msg='That\'s all Folks!')
```

Produces

```bash
# Use default configfy.ini file (missing greetings section)...
# Current config: OrderedDict([('global', {'another_name': 'Suzan Flusan', 'language': 'spanish'})])
Hello Bob, I am Suzan Flusan!
# 2018-08-01 17:45:53,834 - configfy - WARNING - Config section greetings_section not found!
Hello Tom! How are you doing?
Goodby!

# Changing config to "another_config.ini" ...
After setting new config file, current config: OrderedDict([('global', {'language': 'spanish', 'msg': 'A goodby message! Ignored'}), ('greetings_section', {'language': 'german'})])
Hello Bob, I am Pedro!
Hallo Tom! Wie gehts?
Goodby!

# Specifying kwargs, overwriting config settings...
Hello Bob, I am Alfredo!
Zdravo Tom! Kako si?
That's all Folks!
```

# Complete config replacement
This is a complete example making use of configfy as a general tool to replace
the configuration file for an application. The source code can be found in ./doc

```python
import click
import configfy
from configfy import configfy as cfy

# Two user functions that get their kwargs from the current config file
@cfy
def user_function1(kw1=23, name1=''):
    print('Calling user_function1(%s, %s) ...' % (kw1, name1))

@cfy
def user_function2(kw2=None, name2=''):
    print('Calling user_function2(%s, %s) ...' % (kw2, name2))


# Use the excellent click library to handle program arguments
@click.group()
@click.version_option(0.1)
@click.option('-v', '--verbose', count=True)
@click.option('--config', default='configfy.ini', help='Specify the configfy file to use')
def example(verbose, config):
    """
    Enabling sub commands
    """
    # Load config file
    configfy.set_active_config_file(config)

    global config_file
    config_file = config


@example.command()
def ex1():
    user_function1()


@example.command()
def ex2():
    user_function2()


if __name__ == '__main__':
    example()

```

config file:
```ini
[global]
# Pass a number and a list
kw1 = 1001
name1 = ['l', 'i', 's', 't']

# Pass a dict and a set
kw2 = {'d': 42}
# Note: passing set(1, 2, 3) wont work. It will be passed as a string
name2 = {1, 2, 3}
```

## Usage
```bash
> python complete_example.py --config complete_example.ini ex1
Calling user_function1(1001, ['l', 'i', 's', 't']) ...

> python complete_example.py --config complete_example.ini ex2
Calling user_function2({'d': 42}, {1, 2, 3}) ...
```



# Debugging
Debugging functions augmented with configfy can be tricky because instead of stepping
directly into a user function modified by configfy, the debugger will enter the
configfy library code first.

What one can do, is make the debugger "skip" the configfy library code.

## pdb
```python
import pdb
from configfy import configfy as cfy    

@cfy
def fuu(kw_me=42):
    print(kw_me)

if __name__ == '__main__':
    # load pdb, making use of the skip parameter
    pdb.Pdb(skip=['configfy.*']).set_trace()
    fuu()
```

## pudb
```python
import pudb
from configfy import configfy as cfy

# Prevent pudb from stepping into the decorator library code
pudb._get_debugger(skip=['configfy.*'])


@cfy
def fuu(kw_me=42):
    print(kw_me)

if __name__ == '__main__':
    pudb.set_trace()
    fuu()
```

# Overhead
Try it out yourself! Run

> cd doc \
> python overhead.py

I got

```bash
Comparing performance ... this can take a while.
native: 11.863 sec
configfy+config 11.953 sec
configfy 12.160 sec
```


# Author
I happy to receive any feedback or comments on github or privately to manuel.pasieka@protonmail.ch

## Why I wrote this module
I wrote this library because I often have to write prototypes in a *scientific* settings, in which it is unclear upfront what goals to achieve.

It often happened to me that I had to introduce additional parameters and options to functions deep down in the application flow, in order to make its behavior alterable by the user. One can do this by either some global config file, or parse program arguments and pass them through multiple layers to the desired functions.

In order to make those steps easier and speed things up, I wrote this library which enables one to post-hoc add keyword arguments to any function in the codebase, and expose them to the user via a simple config file.

# License
MIT