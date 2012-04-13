import os
import sys
from collections import defaultdict

from pysource.log import get_logger
logger = get_logger('pysource.graph.space')

from pysource.graph.installer import (install_package, uninstall_package,
        FailedToInstall)

# File was found, but it throws an error when it's imported..
class FileExecutionError(Exception):
    pass

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
            try:
                install_package(name)
            except FailedToInstall:
                raise ImportError
            return find_module_under(name)

    def path_of_module(self, module):
        path, _ = extract_path_and_type(module)
        return path

    def find_relative_import(self, importer_path, name):
        importer_dir = os.path.dirname(importer_path)
        importer_dirs = build_full_paths(importer_dir)
        try_names = list(import_name_generator(name))
        for try_name in try_names:
            try:
                return find_module_under(try_name, importer_dirs)
            except ImportError:
                continue
        # Check if the file really exists
        if any(os.path.isfile(os.path.join(a_dir, try_names[-1] + '.py'))
                for a_dir in importer_dirs):
            raise FileExecutionError
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
        try:
            __import__(name)
        except ImportError:
            logger.debug('absolute import `%s` failed', name)
            raise
        except:
            raise FileExecutionError
        return sys.modules[name]
    else:
        try:
            old_sys_path = sys.path[:]
            if isinstance(root_path, list):
                sys.path.extend(root_path)
            else:
                assert isinstance(root_path, basestring)
                sys.path.append(root_path)
            try:
                __import__(name)
            except ImportError as e:
                logger.debug('relative import `%s` under %s failed (%s)', name,
                        sys.path, e)
                raise
            except BaseException as e:
                logger.debug('error when running %s: %s', name, e)
                raise FileExecutionError
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
    for i in xrange(nb_parts, nb_parts - 2, -1):
        yield_name = '.'.join(parts[:i])
        if not yield_name: # empty module name
            continue
        else:
            logger.debug('import generater: %s -> %s', name, yield_name)
            yield yield_name

# /foo/bar -> [/foo/bar, /foo, /]
def build_full_paths(a_dir):
    dirs = [a_dir]
    while True:
        # Try go upper stairs once for each time.
        if a_dir == '/':
            break
        a_dir = os.path.normpath(os.path.join(a_dir, '../'))
        dirs.append(a_dir)
    return dirs

