import sys
sys.path.append('../../../')

import cPickle as pickle
import json
from pysource.log import get_logger
from pysource.graph.space import Space
from pysource.graph.builder import GraphBuilder

def dump_graph(graph, f):
    clean_graph = dict((pkg.name, pkg.dependencies)
                       for pkg in graph.itervalues())
    pickle.dump(clean_graph, f)

def load_graph(f):
    return pickle.load(f)

logger = get_logger('main-script')

INPUT_FILE = 'modules.json'

with open(INPUT_FILE) as f:
    modules = json.load(f).keys()

modules = modules[:50]
logger.warn('modules=%s', modules)

OUTPUT_FILE = 'modules-graph.p'

MAX_NUM_PACKAGES = 200
logger.warn('max_num_packages=%d', MAX_NUM_PACKAGES)

builder = GraphBuilder(Space(), modules, max_num_package=MAX_NUM_PACKAGES)
try:
    builder.build()
except KeyboardInterrupt:
    pass

with open(OUTPUT_FILE, 'w') as f:
    dump_graph(builder.finished_packages, f)

