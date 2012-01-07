import itertools
from pysource.source import parse
from pysource.astanalysis import (format_import_node, extract_import_node,
                                  does_access_modules, extract_attr_chain,
                                  extract_attr_node)

def test_extract_import():
    code = '''
    import foo.bar
    def foo():
        def bar():
            from modulename import funcname
    '''
    import_nodes = extract_import_node(parse(code))
    import_names = (format_import_node(node) for node in import_nodes)
    import_names = itertools.chain.from_iterable(import_names)
    #
    assert sorted(import_names) == sorted(['foo.bar', 'modulename.funcname'])

def test_extract_attr():
    code = '''
    import sys
    sys.stdin.write('hello, world!\\n')
    '''
    module_node = parse(code)
    import_nodes = extract_import_node(module_node)
    import_names = (format_import_node(node) for node in import_nodes)
    import_names = set(itertools.chain.from_iterable(import_names))
   
    attr_nodes = extract_attr_node(module_node)
    predicate = lambda node: does_access_modules(node, import_names)
    module_accessors = itertools.ifilter(predicate, attr_nodes)
    attr_chains = list(extract_attr_chain(node) for node in module_accessors)
    sys_stdin = ['sys', 'stdin', 'write']
    assert sys_stdin in attr_chains
    assert sys_stdin[:-1] in attr_chains

