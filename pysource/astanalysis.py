import ast
import itertools

class ModuleAccessor(object):
    def __init__(self, path, is_base=True):
        self.path = path
        self.is_base = is_base

    def __repr__(self):
        if self.is_base:
            return '<Module %s>' % self.path
        else:
            return '<Attr %s>' % self.path

    def get(self, name):
        return ModuleAccessor('%s.%s' % (self.path, name), is_base=False)

class ModuleContext(object):
    """ A module namespace that manages imported modules and their
        aliases. Useful for analyzing module attribute accesses.
    """
    def __init__(self, import_nodes):
        # data Namespace = Namespace (dict str Namespace)
        #                | Module
        self.ns = {}
        alias_pairs = itertools.imap(_extract_import_alias_pairs, import_nodes)
        for key, value in itertools.chain.from_iterable(alias_pairs):
            _populate_namespace(key, ModuleAccessor(value), self.ns)

    def get(self, name):
        """ str -> ModuleAccessor
        """
        return self.get_by_chain(name.split('.'))

    def get_by_chain(self, attr_chain):
        """ [str] -> Either ModuleAccessor KeyError
        """
        ns = self.ns
        for attr in attr_chain:
            ns = ns.get(attr)
            if ns is None:
                raise KeyError(attr)
        return ns

    def access(self, attr_node):
        """ ast.Node -> Maybe ModuleAccessor
        """
        attr_chain = _extract_attr_chain(attr_node)
        if attr_chain is None:
            return None
        try:
            return self.get_by_chain(attr_chain)
        except KeyError:
            return None

def extract_import_node(node):
    """ :: ast.Node -> [ast.Node]
    """
    return _extract_node(node, _is_import_node)

def extract_attr_or_name_node(node):
    """ :: ast.Node -> [ast.Node]
    """
    return _extract_node(node, _is_attr_or_name_node)

# ---------------------------------------------------------------------------

def _extract_attr_chain(node):
    """ :: ast.Node -> Maybe [str]
    """
    attr_chain = []
    while isinstance(node, ast.Attribute):
        attr_chain.append(node.attr)
        node = node.value
    #
    if isinstance(node, ast.Name):
        attr_chain.append(node.id)
        return list(reversed(attr_chain)) # eg: ['sys', 'stdin', 'write']
    else:
        return None # is not an attr chain that based on NameNode


def _populate_namespace(key, value, output=None):
    """ (str, a, Maybe (dict str a)) -> dict str a

        Dots in key are treated as namespace separator.
    """
    if output is None:
        output = {}
    if '.' in key:
        front, back = key.split('.', 1)
        if front not in output or not isinstance(output[front], dict):
            # create if empty, or override if not a dict.
            output[front] = {}
        _populate_namespace(back, value, output[front])
    else:
        output[key] = value
    return output

def _extract_import_alias_pairs(node):
    """ :: ast.Node -> [(str, str)]
    """
    if isinstance(node, ast.Import):
        return itertools.imap(_extract_alias_pair, node.names)
    else:
        assert isinstance(node, ast.ImportFrom)
        alias_pairs = itertools.imap(_extract_alias_pair, node.names)
        return ((name, '%s.%s' %  (node.module, modulepath))
                for (name, modulepath) in alias_pairs)

def _extract_alias_pair(alias):
    """ :: ast.Node -> (str, str)
        
        Returns a pair of (globalname, modulepath) for this alias node.
    """
    if alias.asname is not None:
        return (alias.asname, alias.name)
    else:
        return (alias.name, alias.name)

def _extract_node(node, predicate):
    """ :: (ast.Node, ast.Node -> bool) -> [ast.Node]
    """
    return itertools.ifilter(predicate, ast.walk(node))

def _is_import_node(node):
    """ :: ast.Node -> bool
    """
    return isinstance(node, (ast.Import, ast.ImportFrom))

def _is_attr_or_name_node(node):
    """ :: ast.Node -> bool
    """
    return isinstance(node, (ast.Attribute, ast.Name))

