def configfy_func(func):
    def func_wrapper(*args, **kwargs):
        print(f'Callng {func} with {args} and {kwargs}')
        return func(*args, **kwargs)
    return func_wrapper

from . import settings
import functools
import inspect

class configfy_class(object):
    def __init__(self, *args, **kwargs):
        print('Init configfy_class ...')
        print(f'args={args}, kwargs={kwargs}')
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

        active_config = settings.get_active_config()

        print(f'Called {self.func} on config {active_config} with {args} {kwargs} ...')
        return self.func(*args, **kwargs)

    @staticmethod
    def __get_kw_args(func):
        S = inspect.signature(func)
        kw = [param for param in S.parameters.keys() if S.parameters[param].default is not inspect._empty]
        return kw

