def configfy_func(func):
    def func_wrapper(*args, **kwargs):
        print(f'Callng {func} with {args} and {kwargs}')
        return func(*args, **kwargs)
    return func_wrapper

from . import configfile
import functools
import inspect

class configfy_class(object):
    def __init__(self, *args, **kwargs):
        print('Init configfy_class ...')
        print(f'args={args}, kwargs={kwargs}')

        if 'section' in kwargs:
            self.section = kwargs['section']
        else:
            self.section = None

        self.needs_wrapping = False
        if args is ():
            print('Complex decorator')
            self.needs_wrapping = True
        else:
            print('Simple decorator')
            self.func = args[0]
            functools.update_wrapper(self, self.func)
            self.kwargs = self.__get_kw_args(self.func)
            print(f'Function has kw {self.kwargs}')

    def __call__(self, *args, **kwargs):
        if self.needs_wrapping:
            self.needs_wrapping = False
            self.func = args[0]
            functools.update_wrapper(self, self.func)
            self.kwargs = self.__get_kw_args(self.func)
            print(f'Function has kw {self.kwargs}')
            return self

        # Get current config, and check which kwargs are relevant for this function
        config = configfile.get_config(self.section)
        kwargs_in_config = [kwarg for kwarg in self.kwargs if kwarg in config]

        # Build a new kwarg dict with the values from the config
        new_kwargs = {kwarg: config[kwarg] for kwarg in kwargs_in_config}

        # Overwrite them with any passed arguments; passed arguments have priority!
        new_kwargs.update(kwargs)

        print(f'Called {self.func} with {args} {new_kwargs} ...')
        return self.func(*args, **new_kwargs)

    @staticmethod
    def __get_kw_args(func):
        S = inspect.signature(func)
        kw = [param for param in S.parameters.keys() if S.parameters[param].default is not inspect._empty]
        return kw

