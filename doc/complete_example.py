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
