# Configfy
Decorator library to expose keyword arguments through config files

Configfy is a prototyping library that enables fast exposure of function parameters to the user in order modify program behavior without having to handle argument parsing or control the flow of config options through your program. It is implemented as a decorator library that makes use of the python configparser module.

Hostet on [github](https://github.com/mapa17/configfy)

* [Installation](##Installation) How to install configfy
* [Examples](##Examples) Look at a simple example
* [Performance overhead](##Overhead) Whats the additional computational cost?
* [Reasons for developing this library](##Why) What is it good for?

## Installation
Configfy is best installed using pip

```bash
    pip install configfy
```

## Examples

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
another_name = Suzan Flusan
```

produces

```bash
Hello Bob, I am Suzan Flusan!
```

Note: Be aware that the library expects the presence of a config file (./configfy.ini) containing at least the empty section [global].

## More Examples
Show how to specify sections to use in config files and how the config file can be changed during runtime, or specified in the decorator.

> From docs/example.py
```python
import configfy
from configfy import configfy as cfy 
from pudb import set_trace as st

@cfy
def hello(name, another_name='Pedro'):
    """Be nice and say hello 
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

print('# Use default configfy.ini file (missing greetings section)...')
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
```

Produces

```bash
# Use default config.ini file (missing greetings section)...
Hello Bob, I am Suzan Flusan!
WARNING:root:Config section greetings_section not found!
Hello Tom! How are you doing?
Goodby!

# Changing config to "another_config.ini" ...
Hello Bob, I am Pedro!
Hallo Tom! Wie gehts?
Goodby!

# Specifying kwargs, overwriting config settings...
Hello Bob, I am Alfredo!
Zdravo Tom! Kako si?
Thats all Folks!
```

## Overhead
Try it out yourself! Run

> python doc/overhead.py

I got

```bash
Comparing performance ... this can take a while.
native: 11.863 sec
configfy+config 11.953 sec
configfy 12.160 sec
```

## Author
I happy to receive any feedback or comments on github or privatly to manuel.pasieka@protonmail.ch

## Why
I wrote this library because I often have to write prototypes in a *scientific* settings, in which it is unclear upfront which goals to achieve.

I therefore often have to introduce additional parameters and options to some function deep down in the application flow, and in order to make its behavior alterable by the user, one has to either have some global config file, or pass arguments from the user input to that part of the execution.

In order to make those steps easier and speed things up, I wrote this library which enables one to post-hoc add keyword arguments to any function in the codebase, and expose them to the user via a simple config file.