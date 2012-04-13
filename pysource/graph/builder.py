""" Non-incremental graph builder.
"""

from collections import deque

from pysource.graph.model import Package
from pysource.graph.space import FileExecutionError
from pysource.log import get_logger

logger = get_logger('pysource.graph.builder')

class GraphBuilder(object):
    def __init__(self, space, root_package_name, max_num_package):
        self.space = space
        if isinstance(root_package_name, list):
            self.root_packages = [Package(self.space, name)
                                  for name in root_package_name]
        else:
            self.root_packages = [Package(self.space, root_package_name)]
        self.max_num_package = max_num_package


    def build(self):
        packages_to_be_resolved = deque(self.root_packages)
        self.finished_packages = {}
        self.failed_packages = {}

        while (packages_to_be_resolved and
                len(self.finished_packages) < self.max_num_package):
            package = packages_to_be_resolved.popleft()
            try:
                package.import_toplevel()
            except (ImportError, FileExecutionError):
                self.failed_packages[package.name] = package
                logger.warn('package %s failed to import.', package.name)
                continue
            package.locate_submodules()
            package.resolve_dependencies()
        
            self.finished_packages[package.name] = package
            for dep_name in package.dependencies:
                if (dep_name not in self.finished_packages and
                        dep_name not in self.failed_packages):
                    packages_to_be_resolved.append(
                            Package(self.space, dep_name))
                    #logger.warn('package %s added.', dep_name)
            logger.info('package %s resolved. (%d/%d)', package.name,
                    len(self.finished_packages), self.max_num_package)
        #

