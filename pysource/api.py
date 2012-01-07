import itertools
from source import parse as parse_source
from astanalysis import (format_import_node, extract_import_node,
                         does_access_modules, extract_attr_chain,
                         extract_attr_node)

def get_import_names(module_node):
    """ :: ast.Node -> [str]

        Returns an iterable that contains module names that are
        imported in the source string.
    """
    import_nodes = extract_import_node(module_node)
    import_names = (format_import_node(node) for node in import_nodes)
    return itertools.chain.from_iterable(import_names)

def get_module_accessors(module_node):
    """ :: ast.Node -> [[str]]
        
        Returns an iterable that contains all attribute accesses to
        modules imported in the given ast node.
    """
    import_names = set(get_import_names(module_node))
    #
    attr_nodes = extract_attr_node(module_node)
    predicate = lambda node: does_access_modules(node, import_names)
    module_accessors = itertools.ifilter(predicate, attr_nodes)
    return (extract_attr_chain(node) for node in module_accessors)

