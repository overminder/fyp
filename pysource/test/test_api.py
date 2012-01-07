import py
from pysource.api import parse_source, get_import_names, get_module_accessors

def test_get_import_names():
    code = '''
    import foo.bar
    def foo():
        def bar():
            from modulename import funcname
    '''
    module_node = parse_source(code)
    import_names = list(get_import_names(module_node))
    #
    assert 'foo.bar' in import_names
    assert 'modulename.funcname' in import_names

def test_extract_attr():
    code = '''
    import sys
    sys.stdin.write('hello, world!\\n')
    '''
    module_node = parse_source(code)
    module_accessors = list(get_module_accessors(module_node))
    #
    assert 'sys.stdin' in module_accessors
    assert 'sys.stdin.write' in module_accessors

@py.test.fail('this is a bug that will be fixed soon.')
def test_extract_attr_with_from():
    code = '''
    from sys import stdin
    stdin.write('hello, world!\\n')
    '''
    module_node = parse_source(code)
    module_accessors = list(get_module_accessors(module_node))
    #
    assert 'sys.stdin.write' in module_accessors

