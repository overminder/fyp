import pytest
from pysource.graph.node import ModuleDepNode

def test_resolve_pip():
    node = ModuleDepNode('pip')
    assert node.is_installed()
    node.resolve_deps()
    assert len(node.deps) > 3 # pip should have many dependencies

@pytest.mark.skipif('1')
def test_resolve_flask():
    node = ModuleDepNode('flask')
    assert not node.is_installed()
    try:
        node.install()
        node.resolve_deps()
        assert len(node.deps) > 3 # flask should also have many dependencies
    finally:
        node.uninstall()

