from .context import configfy
from configfy import configfy as cfy

@cfy
def adder0(a, b):
    """Adder 
    """
    return a + b


@cfy
def adder1(a, b, adder1_offset=0):
    """Adder + offset 
    """
    return (a + b) + adder1_offset


@cfy(config='./tests/test_config2.ini')
def adder2(a, b, adder2_offset=0):
    """Adder + offset 
    """
    return (a + b) + adder2_offset


### Tests ###


def test_adder0():
    """Test function without kwargs
    """
    assert adder0(1, 1) == 2, 'Configfy breaks basic function'

def test_adder1():
    """Test untouched kwargs
    """
    assert adder1(1, 1) == 2, 'Configfy breaks basic function'

def test_adder1_config():
    """Test adder1_offset kwarg from config
    """
    configfy.set_active_config_file('./tests/test_config.ini')
    assert adder1(1, 1) == 3, 'Offset not read from config!'

def test_adder1_overwrite():
    """Test adder1_offset overwrite
    """
    configfy.set_active_config_file('./tests/test_config.ini')
    assert adder1(1, 1, adder1_offset=100) == 102, 'kwarg overwrite does not work!'

def test_adder2():
    """Test adder2
    """
    assert adder2(1, 1) == 102, 'Specifying config file in decorater failed!'


def test_adder2_change_config():
    """Test to change config for adder2
    """
    configfy.set_active_config_file('./tests/test_config2.ini')
    assert adder2(1, 1) == 102, 'Does not keep config settings!'

def test_adder2_overwrite():
    """Test overwrite for adder2
    """
    assert adder2(1, 1, adder2_offset=0) == 2, 'kwarg overwrite does not work!'

assert adder2(1, 1) == 102, 'Specifying config file in decorater failed!'
