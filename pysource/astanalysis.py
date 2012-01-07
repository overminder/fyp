import ast

def format_import_node(node):
    """ :: ast.Node -> (str)
    """
    if isinstance(node, ast.Import):
        return (alias.name for alias in node.names)
    else:
        assert isinstance(node, ast.ImportFrom)
        return ('%s.%s' % (node.module, alias.name) for alias in node.names)

def extract_import_node(node):
    """ :: ast.Node -> (ast.Node)
    """
    for child in ast.walk(node):
        if isinstance(child, (ast.Import, ast.ImportFrom)):
            yield child

