from .context import configfy

#@configfy.configfy_func
@configfy.configfy_class
def adder(a, b, some_option='oki'):
    print('In adder ...')
    return a + b

adder(1, 4)
