import networkx
from matplotlib import pyplot

class Viewer(object):
    def __init__(self, packages):
        self.packages = packages

    def to_networkx_graph(self):
        g = networkx.Graph()
        for name in self.packages.iterkeys():
            g.add_node(name)
        for package in self.packages.itervalues():
            g.add_edges_from([(package.name, dep) for dep in
                              package.dependencies])
        return g

    def output_image(self, path):
        g = self.to_networkx_graph()
        pos = networkx.spring_layout(g)
        networkx.draw(g, pos)
        pyplot.show()
        pyplot.savefig(path)

