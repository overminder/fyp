import ast
import itertools

def format_import_node(node):
    """ :: ast.Node -> [str]
    """
    if isinstance(node, ast.Import):
        return (alias.name for alias in node.names)
    else:
        assert isinstance(node, ast.ImportFrom)
        return ('%s.%s' % (node.module, alias.name) for alias in node.names)

def does_access_modules(node, import_names):
    """ :: (ast.Node, [str]) -> Bool
    """
    while isinstance(node, ast.Attribute):
        node = node.value
    #
    if not isinstance(node, ast.Name):
        return False
    return node.id in import_names

def extract_attr_chain(node):
    """ :: ast.Node -> [str]
    """
    attr_chain = []
    while isinstance(node, ast.Attribute):
        attr_chain.append(node.attr)
        node = node.value
    #
    assert isinstance(node, ast.Name)
    attr_chain.append(node.id)
    return list(reversed(attr_chain)) # eg: ['sys', 'stdin', 'write']

def extract_import_node(node):
    """ :: ast.Node -> [ast.Node]
    """
    return extract_node(node, is_import_node)

def extract_attr_node(node):
    """ :: ast.Node -> [ast.Node]
    """
    return extract_node(node, is_attr_node)

# ---------------------------------------------------------------------------

def extract_node(node, predicate):
    """ :: (ast.Node, ast.Node -> bool) -> [ast.Node]
    """
    return itertools.ifilter(predicate, ast.walk(node))

def is_import_node(node):
    """ :: ast.Node -> bool
    """
    return isinstance(node, (ast.Import, ast.ImportFrom))

def is_attr_node(node):
    """ :: ast.Node -> bool
    """
    return isinstance(node, ast.Attribute)

