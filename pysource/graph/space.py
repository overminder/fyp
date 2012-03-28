import os
import sys
from collections import defaultdict

from pysource.graph.installer import install_package, uninstall_package

class Space(object):
    def __init__(self):
        self.packages = {} # name -> package_node
        self.files = {} # path -> package_node
        self.deferred_deps = [] # [(import_name, importer_path)]
        self.failures = defaultdict(lambda: [])

    def find_package(self, name):
        try:
            return find_module_under(name)
        except ImportError:
            # Package not found: installed it
            install_package(name)
            return find_module_under(name)

    def path_of_module(self, module):
        path, _ = extract_path_and_type(module)
        return path

    def find_relative_import(self, importer_path, name):
        importer_dir = os.path.dirname(importer_path)
        for try_name in import_name_generator(name):
            try:
                return find_module_under(try_name, importer_path)
            except ImportError:
                continue
        raise ImportError

    def find_absolute_import(self, name):
        for try_name in import_name_generator(name):
            try:
                return find_module_under(try_name)
            except ImportError:
                continue
        raise ImportError


# Helper functions
def find_module_under(name, root_path=None):
    if name.split('.')[0] == 'debug':
        raise ImportError # never import debug

    if not root_path:
        __import__(name)
        return sys.modules[name]
    else:
        try:
            old_sys_path = sys.path[:]
            sys.path.append(root_path)
            __import__(name)
            return sys.modules[name]
        except OSError:
            # Huh? no such root path?
            raise ImportError
        finally:
            sys.path[:] = old_sys_path

def is_builtin_module(module):
    return ('built-in' in repr(module) or
            module.__name__ == '__main__')

def extract_path_and_type(module):
    if hasattr(module, '__path__'):
        # Only package has a __path__ attribute, which is a list.
        # @see docs.python.org/tutorial/modules.html
        return module.__path__[0], 'package'
    elif hasattr(module, '__file__'):
        # Plain Python module has only __file__ attribute.
        return module.__file__, 'module'
    else:
        # We can ignore Python builtin module
        assert is_builtin_module(module)
        raise ValueError('Built-in module has no path.')


# e.g., for 'sys.stdout', we will try 'sys.stdout' then 'sys'
def import_name_generator(name):
    parts = name.split('.')
    nb_parts = len(parts)
    for i in xrange(nb_parts, nb_parts - 1, -1):
        yield '.'.join(parts[:i])

