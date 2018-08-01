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
Configfy::Warning: Config section greetings_section not found!
Hello Tom! How are you doing?
Goodby!

# Changing config to "another_config.ini" ...
After setting new config file, current config: OrderedDict([('global', {'language': 'spanish'}), ('greetings_section', {'language': 'german'})])
Hello Bob, I am Pedro!
Hallo Tom! Wie gehts?
Goodby!

# Specifying kwargs, overwriting config settings...
Hello Bob, I am Alfredo!
Zdravo Tom! Kako si?
That's all Folks!
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
I wrote this library because I often have to write prototypes in a *scientific* settings, in which it is unclear upfront what goals to achieve.

It often happened to me that I had to introduce additional parameters and options to functions deep down in the application flow, in order to make its behavior alterable by the user. One can do this by either some global config file, or parse program arguments and pass them through multiple layers to the desired functions.

In order to make those steps easier and speed things up, I wrote this library which enables one to post-hoc add keyword arguments to any function in the codebase, and expose them to the user via a simple config file.

## License
MIT