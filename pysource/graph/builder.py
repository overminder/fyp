""" Non-incremental graph builder.
"""
from pysource.graph.node import PackageNode
from pysource.graph.installer import FailedToInstall
from collections import deque

class GraphBuilder(object):
    def __init__(self, root_package_name, max_num_nodes):
        self.nodes = {} # maps package name to package node
        self.root = PackageNode(root_package_name)
        self.max_num_nodes = max_num_nodes
    
    def build(self):
        nodes_to_expand = deque()
        nodes_to_expand.append(self.root)
        failures = {}

        while len(self.nodes) < self.max_num_nodes:
            # Get one unexpanded node from the queue
            if not nodes_to_expand:
                break
            node = nodes_to_expand.popleft()

            # Download if not installed.
            if not node.is_installed():
                try:
                    node.install()
                except FailedToInstall as e:
                    failures[e.package_name] = node
                    continue

            # Parse and enqueue its dependencies.
            node.resolve_deps()
            if node.deps:
                for package_name in node.deps:
                    if (package_name not in self.nodes and
                            package_name not in failures):
                        nodes_to_expand.append(PackageNode(package_name))

            # Finish this node.
            self.nodes[node.name] = node
        #
        return failures

