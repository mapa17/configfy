import configfy
from pudb import set_trace as st

#@configfy.configfy_func
@configfy.configfy_class
def adder(a, b, some_option='oki'):
    """Some adder doc
    """

    print('In adder ...')
    return a + b

@configfy.configfy_class(config='mamamia.ini', section='Blaa_section')
def multi(i, j, even_more='none'):
    """Some multi doc ...
    """
    print('In multi ...')
    return i * j

#st()
print(adder(1, 1))
print(multi(10, 3, even_more='blaa'))
#st()
configfy.set_active_config('another.ini')
print(adder(2, 2))

print(adder(3, 3, some_option='new args'))
