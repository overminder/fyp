import os
from pysource.graph.installer import FailedToInstall
from pysource.graph.space import (is_builtin_module, FileExecutionError,
        extract_path_and_type)
from pysource.log import get_logger
from pysource.api import get_import_names

logger = get_logger('pysource.graph.model')

class Package(object):
    """ A package is a top-level source folder.
        It contains several submodules.
    """
    pymodule = None # :: PyModule
    rootpath = None # :: str
    submodules = None # :: [Module]
    dependencies = None # :: [str]

    def __init__(self, space, name):
        self.space = space # :: Space
        self.name = name # :: str

    def import_toplevel(self):
        """ import this package.
        """
        self.pymodule = self.space.find_package(self.name)
        if not is_builtin_module(self.pymodule):
            self.rootpath = self.space.path_of_module(self.pymodule)
            logger.info('%s at %s', self.name, self.rootpath)

    def locate_submodules(self):
        """ find all .py files in the package folder.
        """
        sources = []
        # Find all source files.
        if self.rootpath is not None:
            for dirname, _, filenames in os.walk(self.rootpath):
                for filename in filenames:
                    if filename.endswith('.py'):
                        sources.append(os.path.normpath(os.path.join(dirname,
                            filename)))
        self.submodules = [Module.from_path(self, path) for path in sources]
        self.sources = sources

    def resolve_dependencies(self):
        dependency_package_names = set()
        for submodule in self.submodules:
            submodule.find_imports()
            for import_object in submodule.imports:
                if isinstance(import_object, AbsoluteImport):
                    dependency_package_names.add(
                            import_object.get_package_name())
        self.dependencies = dependency_package_names

class Module(object):
    """ A module is a python source file.
        It contains some source text.
    """
    imports = None # :: [AbstractImport]

    def __repr__(self):
        return '<Module %s>' % self.filepath

    @staticmethod
    def from_path(package, path):
        self = Module()
        self.filepath = path # :: str
        self.package = package # :: Package
        self.space = package.space
        with open(path) as f:
            self.content = f.read() # :: str
        return self

    def find_imports(self):
        from pysource.api import parse_source
        try:
            source_ast = parse_source(self.content)
        except SyntaxError:
            logger.warn('`%s...` is not parsable!', self.content[:100])
            self.imports = []
            return

        import_names = set(get_import_names(source_ast))
        imports = []

        for import_name in import_names:
            try:
                try:
                    import_object = import_module(self, import_name)
                except ImportError:
                    # Probably because that the package is not installed
                    package_name = import_name.split('.')[0]
                    try:
                        import_object = AbsoluteImport.from_package(
                                self.space.find_package(package_name),
                                import_name)
                    except ImportError:
                        continue # Just ignore this import for now.
            except FileExecutionError:
                continue
            imports.append(import_object)
        #
        self.imports = imports


class AbstractImport(object):
    """ A file has several imports.
    """
    importpath = None # str, eg, 'sys.path'
    pymodule = None # :: PyModule

class RelativeImport(AbstractImport):
    """ An import that can only be found relatively in package hierarchy
    """

class AbsoluteImport(AbstractImport):
    """ An import that can be directly found in sys.path.
    """
    @staticmethod
    def from_package(pymodule, importpath):
        import_object = AbsoluteImport()
        import_object.importpath = importpath
        import_object.pymodule = pymodule
        return import_object

    def get_package_name(self):
        return self.importpath.split('.')[0]

def import_module(importer, name):
    space = importer.space
    try:
        pymodule = space.find_relative_import(importer.filepath, name)
    except ImportError:
        pymodule = space.find_relative_import(importer.package.rootpath, name)
    if is_builtin_module(pymodule):
        import_object = AbsoluteImport()
        import_object.pymodule = space.find_absolute_import(name)
    else:
        mypath, _ = extract_path_and_type(pymodule)
        if mypath in importer.package.sources:
            # Is a relative import
            import_object = RelativeImport()
        else:
            # Is a absolute import
            import_object = AbsoluteImport()
            import_object.pymodule = space.find_absolute_import(name)
    import_object.importpath = name
    return import_object

