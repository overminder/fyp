import sys
sys.path.append('../../../')

DATA_PATH = 'large-graph.pickle'

MAX_NUM_PACKAGES = 1000

import cPickle as pickle
from pysource.graph.space import Space
from pysource.graph.builder import GraphBuilder

builder = GraphBuilder(Space(), ['pip'], max_num_package=10)
builder.build()

def dump_graph(graph, f):
    clean_graph = dict((k, v.name) for (k, v) in graph.iteritems())
    pickle.dump(clean_graph, f)

def load_graph(f):
    return pickle.load(f)

with open(DATA_PATH, 'w') as f:
    dump_graph(builder.finished_packages, f)

