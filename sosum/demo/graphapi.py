import os
import sys
import math
from django.conf import settings
sys.path.append(os.path.join(settings.SITE_ROOT, '../'))
from pysource.graph.bin.graph_loader import load_knowledge_graph
from pysource.graph.space import Space
from pysource.graph.builder import GraphBuilder
from pysource.api import parse_source, get_import_names

def build_undirected_graph(g):
    from collections import defaultdict
    ung = defaultdict(lambda: set())
    for n, ns in g.iteritems():
        for n2 in ns:
            ung[n].add(n2)
            ung[n2].add(n)
    return ung

G = load_knowledge_graph()
UNG = build_undirected_graph(G)
SPACE = Space()

def gen_subgraph_from_code(code):
    try:
        module = parse_source(code)
    except SyntaxError:
        return {}
    return gen_subgraph_from_keywords(get_import_names(module))

def gen_subgraph_from_keywords(kws):
    graph = {}
    for name in kws:
        if '.' in name:
            name = name.split('.')[0]
        if name in G:
            graph[name] = G[name]

    return graph

def subgraph_distance(g1, g2):
    sum_len = 0
    unique_nodes = set()
    common_nodes = set()
    for n1 in g1:
        for n2 in g2:
            shortest_len = shortest_path(n1, n2, UNG)
            sum_len += shortest_len

    for n1 in g1:
        if n1 in g2:
            common_nodes.add(n1)
        else:
            unique_nodes.add(n1)

    for n2 in g2:
        if n2 not in g1:
            unique_nodes.add(n2)

    return (0.5 * len(common_nodes) / (len(unique_nodes) + 1.0) + 
            0.5 * math.exp(sum_len * 1.0 / (len(g1) * len(g2) + 1.0)))

def shortest_path(n1, n2, g):
    d = dict((n, -1) for n in g) # dist
    unv_set = set(n for n in g)
    curr = n1
    d[curr] = 0
    while n2 in unv_set:
        for neighbour in g[curr]:
            if d[neighbour] == -1:
                d[neighbour] = d[curr] + 1
            elif d[neighbour] > d[curr] + 1:
                d[neighbour] = d[curr] + 1
        unv_set.discard(curr)
        curr = iter(unv_set).next()
    return d[n2]

