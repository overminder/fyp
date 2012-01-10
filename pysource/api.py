import ast
import operator
import itertools
from source import parse as _parse
from astanalysis import (extract_import_node, extract_attr_or_name_node,
                         ModuleContext)

def parse_source(codestring, failfast=True):
    """ :: (str, bool) -> ast.Node

        Returns an ast.Node object. Usually it's an module.
    """
    return _parse(codestring, failfast)

def get_import_names(module_node):
    """ :: ast.Node -> [str]

        Returns an iterable that contains module names that are
        imported in the source string.
    """
    import_nodes = extract_import_node(module_node)
    import_names = itertools.imap(_format_import_node, import_nodes)
    return itertools.chain.from_iterable(import_names)

def get_module_accessors(module_node):
    """ :: ast.Node -> [str]
        
        Returns an iterable that contains all attribute accesses to
        modules imported in the given ast node.
    """
    import_nodes = extract_import_node(module_node)
    module_context = ModuleContext(import_nodes)
    #
    attr_nodes = extract_attr_or_name_node(module_node)
    accessors = itertools.ifilter(bool, itertools.imap(module_context.access,
                                                       attr_nodes))
    return itertools.imap(operator.attrgetter('path'), accessors)

# ---------------------------------------------------------------------------

def _format_import_node(node):
    """ :: ast.Node -> [str]
    """
    if isinstance(node, ast.Import):
        return (alias.name for alias in node.names)
    else:
        assert isinstance(node, ast.ImportFrom)
        return ('%s.%s' % (node.module, alias.name) for alias in node.names)

