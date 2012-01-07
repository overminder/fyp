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
    assert sorted(import_names) == sorted(['foo.bar', 'modulename.funcname'])

def test_extract_attr():
    code = '''
    import sys
    sys.stdin.write('hello, world!\\n')
    '''
    module_node = parse_source(code)
    module_accessors = list(get_module_accessors(module_node))
    #
    wanted = ['sys', 'stdin', 'write']
    assert wanted in module_accessors
    assert wanted[:-1] in module_accessors

