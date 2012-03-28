import os
from pysource.graph.installer import FailedToInstall
from pysource.graph.space import is_builtin_module
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
        source_ast = parse_source(self.content)
        import_names = set(get_import_names(source_ast))
        imports = []

        for import_name in import_names:
            try:
                import_object = RelativeImport.from_name(self, import_name)
            except ImportError:
                try:
                    import_object = AbsoluteImport.from_name(self, import_name)
                except ImportError:
                    # Probably because that the package is not installed
                    package_name = import_name.split('.')[0]
                    try:
                        import_object = AbsoluteImport.from_package(
                                self.space.find_package(package_name),
                                import_name)
                    except FailedToInstall:
                        logger.warn('failed to install %s', import_name)
                        continue # Just ignore for now.
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
    @staticmethod
    def from_name(module, name):
        space = module.space
        try:
            pymodule = space.find_relative_import(module.filepath, name)
        except ImportError:
            pymodule = space.find_relative_import(module.package.rootpath, name)
        import_object = RelativeImport()
        import_object.importpath = name
        return import_object

class AbsoluteImport(AbstractImport):
    """ An import that can be directly found in sys.path.
    """
    @staticmethod
    def from_name(module, name):
        space = module.space
        import_object = AbsoluteImport()
        import_object.pymodule = space.find_absolute_import(name)
        import_object.importpath = name
        return import_object

    @staticmethod
    def from_package(pymodule, importpath):
        import_object = AbsoluteImport()
        import_object.importpath = importpath
        import_object.pymodule = pymodule
        return import_object

    def get_package_name(self):
        return self.importpath.split('.')[0]

