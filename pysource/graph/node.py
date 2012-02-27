import os
import sys
from weakref import WeakSet
from pysource.graph.installer import install_package, uninstall_package
from pysource.api import parse_source, get_import_names

class PackageNode(object):
    def __init__(self, name):
        self.name = name # :: str, the toplevel package name
        self.deps = None # :: Set str, or None for a builtin module/package
        self.importer = None # :: str, full-qualified name of its importer

    def __repr__(self):
        return '#<PackageNode %s deps=%r importer=%r>' % (
                self.name, self.deps, self.importer)

    def is_installed(self):
        try:
            __import__(self.name)
        except ImportError:
            return False
        return True

    def try_relative_import(self, builder):
        if not self.importer:
            return False
        real_import_path = '%s.%s' % (self.importer, self.name)
        try:
            __import__(real_import_path)
            self.name = real_import_path
            builder.add_relative_import(self.importer.split('.')[0],
                    real_import_path)
            return True
        except ImportError:
            return False

    def install(self):
        install_package(self.name)

    def uninstall(self):
        uninstall_package(self.name)

    def get_module(self):
        __import__(self.name)
        return sys.modules[self.name]

    def resolve_deps(self):
        module = self.get_module()
        if is_builtin_module(module):
            return
        path, module_type = extract_path_and_type(module)
        if module_type == 'package':
            self.deps = self._resolve_package_deps(module.__path__[0])
        elif module_type == 'module':
            self.deps = self._resolve_module_deps(module.__file__)

    def _resolve_package_deps(self, root_path):
        deps = set()
        sources = []
        # Find all source files.
        for dirname, _, filenames in os.walk(root_path):
            for filename in filenames:
                if filename.endswith('.py'):
                    sources.append(os.path.join(dirname, filename))
        # For each source file, parse and analyze its content.
        # This way we can find what module it will import.
        for source_path in sources:
            importer_path = os.path.relpath(source_path, root_path)
            importer = 
            for dep in self._resolve_file_deps(source_path):
                deps.add(dep)
        return deps

    def _resolve_module_deps(self, source_path):
        if not source_path.endswith('.py'):
            # May be compiled source file or dynamic library file.
            if source_path.endswith('.pyc'):
                # For compiled source, we may look at its corresponding
                # source file.
                source_path = source_path[:-1] # *.pyc -> *.py
                if not os.path.isfile(source_path):
                    # But if .py file doesn't exit...
                    return set()
            elif source_path.endswith('.so'):
                return set()
            else:
                assert 0, 'unknown module path type: %s' % source_path
        return set(self._resolve_file_deps(source_path))

    def _resolve_file_deps(self, filename):
        """ Returns a list of (import_path, importer_file_name)
        """
        with open(filename) as f:
            content = f.read()
        try:
            parsed = parse_source(content)
        except SyntaxError:
            raise SyntaxError('failed to parse source file `%s\'' % filename)
        for import_name in get_import_names(parsed):
            yield import_name.split('.')[0] # *.py -> *

# Helper functions
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

