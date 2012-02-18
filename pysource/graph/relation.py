from math import sqrt, acos
from itertools import izip

def compute_vector(builder, package_name):
    assert builder.frozen
    node = builder.nodes[package_name]
    vector = [(1 if name in node.deps else 0) for name in builder.node_names]
    node.vector = vector

def angle_between_nodes(n1, n2):
    v1, v2 = n1.vector, n2.vector
    return angle_between_vectors(v1, v2)

# In rad.
def angle_between_vectors(v1, v2):
    product_of_length = sum(v1) * sum(v2)
    dot_product = float(sum(a * b for (a, b) in izip(v1, v2)))
    return acos(dot_product / product_of_length)

