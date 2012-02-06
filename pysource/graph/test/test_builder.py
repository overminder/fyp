from pysource.graph.installer import uninstall_package
from pysource.graph.builder import GraphBuilder

def test_build_pip_deps():
    # pip is a downloaded module.
    builder = GraphBuilder('pip', max_num_nodes=10)
    failures = builder.build()
    assert not failures
    assert len(builder.nodes) == 10
    # Now builder.nodes contains 10 PackageNodes.

def test_build_flask_deps():
    try:
        # flask is a (hopefully) undownloaded module.
        builder = GraphBuilder('flask', max_num_nodes=15)

        failures = builder.build()
        # For flask, there are some failures...
        assert len(builder.nodes) == 15
    finally:
        uninstall_package('flask')

