import networkx
from matplotlib import pyplot

class Viewer(object):
    def __init__(self, builder):
        self.builder = builder

    def to_networkx_graph(self):
        g = networkx.Graph()
        for name in self.builder.nodes:
            g.add_node(name)
        for node in self.builder.nodes.itervalues():
            if node.deps:
                g.add_edges_from([(node.name, dep) for dep in node.deps])
        return g

    def output_image(self, path):
        g = self.to_networkx_graph()
        pos = networkx.spring_layout(g)
        networkx.draw(g, pos)
        pyplot.show()
        pyplot.savefig(path)

