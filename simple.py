import configfy
from pudb import set_trace as st

#@configfy.configfy_func
@configfy.configfy_class
def adder(a, b, some_option='oki'):
    """Some adder doc
    """

    print('In adder ...')
    return a + b

@configfy.configfy_class(config='mamamia.ini', section='specific_section')
def multi(i, j, multi_argument='none'):
    """Some multi doc ...
    """
    print('In multi ...')
    return i * j

print(adder(1, 1))
print(multi(10, 3))

configfy.set_active_config_file('another_config.ini')
print(adder(2, 2))
print(multi(10, 3))

print(adder(3, 3, some_option='Overwriting config options'))
