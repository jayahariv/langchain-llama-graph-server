import pkgutil
import importlib
import inspect

from .base import LLMProvider

def get_providers():
    providers = {}
    pkg = __name__
    for loader, module_name, is_pkg in pkgutil.iter_modules(__path__):
        if module_name == "base":
            continue
        module = importlib.import_module(f"{pkg}.{module_name}")
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, LLMProvider) and obj is not LLMProvider:
                providers[module_name] = obj()
    return providers
