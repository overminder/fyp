import operator
import itertools
from pysource.source import parse
from pysource.astanalysis import (extract_import_node, extract_attr_node,
                                  ModuleContext)

def test_extract_import():
    code = '''
    import foo.bar
    def foo():
        def bar():
            from modulename import funcname as func
    '''
    import_nodes = list(extract_import_node(parse(code)))
    #
    assert len(import_nodes) == 2
    assert import_nodes[0].names[0].name == 'foo.bar'
    assert import_nodes[0].names[0].asname is None
    assert import_nodes[1].module == 'modulename'
    assert import_nodes[1].names[0].name == 'funcname'
    assert import_nodes[1].names[0].asname == 'func'

def test_extract_attr():
    code = '''
    import sys
    sys.stdin.write('hello, world!\\n')
    '''
    module_node = parse(code)
    import_nodes = extract_import_node(module_node)
    module_context = ModuleContext(import_nodes)
   
    attr_nodes = extract_attr_node(module_node)
    accessors = itertools.ifilter(bool, itertools.imap(module_context.access,
                                                       attr_nodes))
    return itertools.imap(operator.attrgetter('path'), accessors)
    sys_stdin = ['sys', 'stdin', 'write']
    assert '.'.join(wanted) in module_accessors
    assert '.'.join(wanted[:-1]) in module_accessors

