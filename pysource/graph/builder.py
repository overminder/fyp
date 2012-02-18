""" Non-incremental graph builder.
"""
from pysource.log import get_logger
from pysource.graph.node import ModuleDepNode
from pysource.graph.installer import FailedToInstall
from collections import OrderedDict

logger = get_logger('pysource.graph.builder')

class GraphBuilder(object):
    frozen = False

    def __init__(self, root_package_name, max_num_nodes):
        self.nodes = {} # maps package name to package node
        self.roots = [ModuleDepNode(root_package_name)]
        self.max_num_nodes = max_num_nodes

    def add_root(self, name):
        self.roots.append(ModuleDepNode(name))

    def freeze(self):
        """ Freeze the graph to make it easier to do vector space model
            analysis on the graph.
        """
        self.frozen = True
        self.node_names = list(self.nodes.iterkeys())
    
    def build(self):
        nodes_to_expand = OrderedDict()
        for root in self.roots:
            nodes_to_expand[root.name] = root
        failures = {}

        while len(self.nodes) < self.max_num_nodes:
            # Get one unexpanded node from the queue
            if not nodes_to_expand:
                break
            # Pop from the left, that is, FIFO.
            (_, node) = nodes_to_expand.popitem(last=False)
            logger.info('resolving module `%s\'' % node.name)

            # Download if cannot find the corresponding module.
            if not node.is_installed():
                if not node.try_relative_import():
                    try:
                        node.install()
                    except FailedToInstall as e:
                        # Save this failure for future inspection.
                        logger.warn('%s -- %s' % (e, node))
                        failures[e.package_name] = (e, node)
                        continue

            # Parse and enqueue its dependencies.
            node.resolve_deps()
            if node.deps:
                # Currently *.pyc and *.so are not resolved.
                # Surely we can execute *.pyc but this is too dangerous.
                for package_name, importer in node.deps:
                    if (package_name not in self.nodes and
                            package_name not in failures and
                            package_name not in nodes_to_expand and
                            package_name != node.name):
                        child_node = ModuleDepNode(package_name)
                        child_node.add_importer(importer)
                        nodes_to_expand[package_name] = child_node

            # Finish this node.
            self.nodes[node.name] = node
            print 'finished node #%d, queue has %d items.' % (
                    len(self.nodes), len(nodes_to_expand))
        #
        return failures

