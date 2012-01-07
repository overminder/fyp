import py
import ast
from pysource.source import parse

def test_parse():
    code = '''
    a = 0
    '''
    module = parse(code)
    assert len(module.body) == 1
    assert isinstance(module.body[0], ast.Assign)

def test_fail_to_parse():
    code = '''
    impot foo.bar # note the syntax error
    '''
    #
    py.test.raises(SyntaxError, parse, code)
    py.test.raises(SyntaxError, parse, code, failfast=False)
