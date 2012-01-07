import itertools
from source import parse
from astanalysis import format_import_node, extract_import_node

def get_import_names(sourcestring):
    """ :: str -> (str)

        Returns an iterable that contains module names that are
        imported in the source string.
    """
    module = parse(sourcestring)
    import_nodes = extract_import_node(module)
    import_names = (format_import_node(node) for node in import_nodes)
    return itertools.chain.from_iterable(import_names)

