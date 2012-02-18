#!/usr/bin/env python

import sys
import path_fix
from pysource.graph.builder import GraphBuilder
from pysource.graph.relation import compute_vector, angle_between_nodes

def main(argv):
    _, library1, library2, max_num_nodes = argv
    builder = GraphBuilder(library1, max_num_nodes=int(max_num_nodes))
    builder.add_root(library2)
    errors = builder.build()
    builder.freeze()

    compute_vector(builder, library1)
    node1 = builder.nodes[library1]
    compute_vector(builder, library2)
    node2 = builder.nodes[library2]
    angle = angle_between_nodes(node1, node2)

    print 'Angle between `%s\' and `%s\' is %f' % (library1, library2, angle)

if __name__ == '__main__':
    main(sys.argv)

