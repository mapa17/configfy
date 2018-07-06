from . import configfile
import functools
import inspect
#from pudb import set_trace as st

class configfy(object):
    def __init__(self, *args, **kwargs):
        # Default flags
        self.new_kwargs = None
        self.needs_wrapping = False
        
        if 'section' in kwargs:
            self.section = kwargs['section']
        else:
            self.section = None

        if 'config' in kwargs:
            self.config = configfile.read_configfile(kwargs['config'])
        else:
            self.config = None

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

            # If config file is specified in decorator, new kwargs can be precalculated!
            if self.config is not None:
                self.new_kwargs = self._get_new_kwargs()
    
            return self

        # Use precalculated kwargs if available
        if self.new_kwargs is None:
            new_kwargs = self._get_new_kwargs()
        else:
            new_kwargs = self.new_kwargs

        # Overwrite them with any passed arguments; passed arguments have priority!
        new_kwargs.update(kwargs)

        # Call target function with altered kwargs
        return self.func(*args, **new_kwargs)
    
    def _get_new_kwargs(self):
        """Helper function that gets kwargs for this function from its config
        
        Returns:
            [OrderedDictionary] -- [kwargs in dictionary]
        """
        # Get a list of kwargs that are present in the config file
        config = configfile.get_config(self.config, self.section)
        kwargs_in_config = [kwarg for kwarg in self.kwargs if kwarg in config]

        # Build a new kwarg dict with the values from the config
        new_kwargs = {kwarg: config[kwarg] for kwarg in kwargs_in_config}
        return new_kwargs

    @staticmethod
    def __get_kw_args(func):
        S = inspect.signature(func)
        kw = [param for param in S.parameters.keys() if S.parameters[param].default is not inspect._empty]
        return kw

