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


### Tests Configfy ###


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


### Tests Configfy subcomponents ###

def test_configfile_parser():
    """Test configfy.configfile.__parse_parameter()
    """
    #print("[abc]: ", configfy.configfile.__parse_parameter('"abc"'))
    # Test basic values
    assert configfy.configfile.__parse_parameter('None') == None, "Parsing parameter failed!"
    assert configfy.configfile.__parse_parameter('none') == None, "Parsing parameter failed!"
    assert configfy.configfile.__parse_parameter('') == None, "Parsing parameter failed!"
    assert configfy.configfile.__parse_parameter('true') == True, "Parsing parameter failed!"
    assert configfy.configfile.__parse_parameter('TrUe') == True, "Parsing parameter failed!"
    assert configfy.configfile.__parse_parameter('false') == False, "Parsing parameter failed!"
    assert configfy.configfile.__parse_parameter('fAlsE') == False, "Parsing parameter failed!"
    
    assert configfy.configfile.__parse_parameter('42') == 42, "Parsing parameter failed!"
    assert configfy.configfile.__parse_parameter('1000.123') == 1000.123, "Parsing parameter failed!"
    assert configfy.configfile.__parse_parameter('"abcd"') == 'abcd', "Parsing parameter failed!"

    # Test simple list constructs
    assert configfy.configfile.__parse_parameter('[]') == [], "Parsing empty list failed!"
    assert configfy.configfile.__parse_parameter("['abc']") == ['abc'], "Parsing list failed!"
    assert configfy.configfile.__parse_parameter("['a', 'b', 'c']") == ['a', 'b', 'c'], "Parsing list failed!"
    assert configfy.configfile.__parse_parameter('[10]') == [10], "Parsing list failed!"
    assert configfy.configfile.__parse_parameter('[23.23]') == [23.23], "Parsing list failed!"
    assert configfy.configfile.__parse_parameter('[10, 11, 12, 13]') == [10, 11, 12, 13], "Parsing list failed!"
    assert configfy.configfile.__parse_parameter('[10, 11.11]') == [10, 11.11], "Parsing list failed!"

    # Test list in lists
    assert configfy.configfile.__parse_parameter('[[10, 20], [100, 200]]') == [[10, 20], [100, 200]], "Parsing list failed!"
    assert configfy.configfile.__parse_parameter("[['abc', 'cdf'], ['ABC', 'CDF']]") == [['abc', 'cdf'], ['ABC', "CDF"]], "Parsing list failed!"
