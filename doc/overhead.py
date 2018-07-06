import time
import timeit
import numpy as np
import configfy
from configfy import configfy as cfy

def do_stuff(kw_arg=13):
    time.sleep(10.0/1000.0)
    return np.random.random()*kw_arg

@cfy()
def configfy_without_config_option(kw_arg=13):
    time.sleep(10.0/1000.0)
    return np.random.random()*kw_arg

@cfy(config='yet_another_config.ini')
def configfy_with_config_option(kw_arg=13):
    time.sleep(10.0/1000.0)
    return np.random.random()*kw_arg

# Set config file
configfy.set_active_config_file('another_config.ini')

# Run enough times
N = 1000
print('\nComparing performance ... this can take a while.')
nativ = timeit.timeit('do_stuff()', number=N, globals=globals())
withconfig = timeit.timeit('configfy_with_config_option()', number=N, globals=globals())
withoutconfig = timeit.timeit('configfy_without_config_option()', number=N, globals=globals())

print(f'native: {nativ:2.3f} sec\nconfigfy+config {withconfig:2.3f} sec\nconfigfy {withoutconfig:2.3f}sec')
