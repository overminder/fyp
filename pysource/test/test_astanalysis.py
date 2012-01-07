import operator
import itertools
from pysource.source import parse
from pysource.astanalysis import (extract_import_node,
                                  extract_attr_or_name_node,
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
   
    attr_nodes = extract_attr_or_name_node(module_node)
    accessors = itertools.ifilter(bool, itertools.imap(module_context.access,
                                                       attr_nodes))
    module_accessors = list(itertools.imap(operator.attrgetter('path'),
                                           accessors))
    assert 'sys.stdin' in module_accessors
    assert 'sys.stdin.write' in module_accessors

def test_module_context():
    code = '''
    from sys import stdin
    from os.path import dirname
    from a.b.c.d import e
    '''
    module_node = parse(code)
    import_nodes = extract_import_node(module_node)
    module_context = ModuleContext(import_nodes)

    assert 'stdin' in module_context.ns
    assert 'dirname' in module_context.ns
    assert 'e' in module_context.ns
    assert module_context.ns['e'].path == 'a.b.c.d.e'

