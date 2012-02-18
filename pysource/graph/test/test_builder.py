import pytest
from pysource.graph.installer import uninstall_package
from pysource.graph.builder import GraphBuilder

def test_build_pip_deps():
    # pip is a downloaded module.
    max_nodes = 10
    builder = GraphBuilder('pip', max_num_nodes=max_nodes)
    failures = builder.build()
    assert len(builder.nodes) == max_nodes
    # Now builder.nodes contains $max_nodes ModuleDepNodes.

@pytest.mark.skipif('1')
def test_build_flask_deps():
    try:
        # flask is a (hopefully) undownloaded module.
        builder = GraphBuilder('flask', max_num_nodes=15)

        failures = builder.build()
        # For flask, there are some failures...
        assert len(builder.nodes) == 15
    finally:
        return
        uninstall_package('flask')

