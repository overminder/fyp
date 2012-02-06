import py
from pysource.graph import installer

def try_import(module_name, expect_failure=True):
    try:
        __import__(module_name)
        succ = True
    except ImportError:
        succ = False

    if succ and expect_failure:
        assert 0, '%s should not be installed' % module_name
    elif not succ and not expect_failure:
        assert 0, '%s should be installed' % module_name

@py.test.skip('too long to run...')
def test_install_flask():
    module = 'flask'
    try:
        try_import(module, expect_failure=True)
        installer.install_package('flask')
        try_import(module, expect_failure=False)
    finally:
        installer.uninstall_package('flask')

