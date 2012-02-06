import os
from pysource.graph.installer import install_package, uninstall_package
from pysource.api import parse_source, get_import_names

class PackageNode(object):
    def __init__(self, name):
        self.name = name
        self.deps = None

    def __repr__(self):
        return '#<PackageNode %s deps=%r>' % (self.name, self.deps)

    def is_installed(self):
        try:
            __import__(self.name)
        except ImportError:
            return False
        return True

    def install(self):
        install_package(self.name)

    def uninstall(self):
        uninstall_package(self.name)

    def resolve_deps(self):
        module = __import__(self.name)
        if hasattr(module, '__path__'):
            # Only package has a __path__ attribute, which is a list.
            # @see docs.python.org/tutorial/modules.html
            self.deps = self._resolve_package_deps(module.__path__[0])
        elif hasattr(module, '__file__'):
            # Plain Python module has only __file__ attribute.
            self.deps = self._resolve_module_deps(module.__file__)
        else:
            # We can ignore Python builtin module
            assert 'built-in' in repr(module)

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
            for dep in self._resolve_file_deps(source_path):
                deps.add(dep)
        return deps

    def _resolve_module_deps(self, source_path):
        if not source_path.endswith('.py'):
            # May be compiled source file or dynamic library file.
            if source_path.endswith('.pyc'):
                # For compiled source, we may look at its corresponding
                # source file.
                source_path = source_path[:-1]
                if not os.path.isfile(source_path):
                    # But if .py file doesn't exit...
                    return set()
            elif source_path.endswith('.so'):
                return set()
            else:
                assert 0, 'unknown module path type: %s' % source_path
        return set(self._resolve_file_deps(source_path))

    def _resolve_file_deps(self, filename):
        with open(filename) as f:
            content = f.read()
        try:
            parsed = parse_source(content)
        except SyntaxError:
            raise SyntaxError('failed to parse %s' % filename)
        for import_name in get_import_names(parsed):
            yield import_name.split('.')[0]

