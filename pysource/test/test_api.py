def test_get_import_names():
    from pysource.api import get_import_names
    code = '''
    import foo.bar
    def foo():
        def bar():
            from modulename import funcname
    '''
    import_names = list(get_import_names(code))
    #
    assert sorted(import_names) == sorted(['foo.bar', 'modulename.funcname'])

