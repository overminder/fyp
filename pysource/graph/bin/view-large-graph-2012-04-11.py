import cPickle as pickle
import networkx
from matplotlib import pyplot

def load_graph(f):
    return pickle.load(f)

INPUT_FILE = 'modules-graph.p'
OUTPUT_FILE = 'modules-graph.png'

with open(INPUT_FILE) as f:
    graph = load_graph(f)

g = networkx.Graph()
for name in graph:
    g.add_node(name)
for pkg, deps in graph.iteritems():
    g.add_edges_from([(pkg, dep) for dep in deps])

pos = networkx.spring_layout(g)
networkx.draw(g, pos)
pyplot.show()
pyplot.savefig(OUTPUT_FILE)

