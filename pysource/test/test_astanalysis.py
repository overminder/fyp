import itertools
from pysource.source import parse
from pysource.astanalysis import format_import_node, extract_import_node

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

