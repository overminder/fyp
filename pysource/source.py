import py
import ast

def parse(codestring, failfast=True):
    """ :: (str, bool) -> ast.Node
    """
    source = py.code.Source(codestring)
    if not source.isparseable() and failfast:
        raise SyntaxError, 'code `\n%s\n` is not parseable.' % codestring
    #
    return source.compile(flag=ast.PyCF_ONLY_AST)

