from . import configfile
import functools
import inspect

class configfy(object):
    def __init__(self, *args, **kwargs):
        if 'section' in kwargs:
            self.section = kwargs['section']
        else:
            self.section = None
        
        if 'config' in kwargs:
           self.config = configfile.read_configfile(kwargs['config'])
        else:
            self.config = None

        self.needs_wrapping = False
        if args is ():
            self.needs_wrapping = True
        else:
            self.func = args[0]
            functools.update_wrapper(self, self.func)
            self.kwargs = self.__get_kw_args(self.func)

    def __call__(self, *args, **kwargs):
        if self.needs_wrapping:
            self.needs_wrapping = False
            self.func = args[0]
            functools.update_wrapper(self, self.func)
            self.kwargs = self.__get_kw_args(self.func)
            return self

        # Get current config or function config, and check which kwargs are relevant for this function
        if self.config is None:
            config = configfile.get_config(self.section)
        else:
            config = self.config
        kwargs_in_config = [kwarg for kwarg in self.kwargs if kwarg in config]

        # Build a new kwarg dict with the values from the config
        new_kwargs = {kwarg: config[kwarg] for kwarg in kwargs_in_config}

        # Overwrite them with any passed arguments; passed arguments have priority!
        new_kwargs.update(kwargs)

        #print(f'Called {self.func} with {args} {new_kwargs} ...')
        return self.func(*args, **new_kwargs)

    @staticmethod
    def __get_kw_args(func):
        S = inspect.signature(func)
        kw = [param for param in S.parameters.keys() if S.parameters[param].default is not inspect._empty]
        return kw

