import pytest
from pysource.graph.installer import uninstall_package
from pysource.graph.model import Package
from pysource.graph.space import Space

def test_pip_deps():
    # pip is a downloaded module.
    space = Space()
    pip = Package(space, 'pip')
    pip.import_toplevel()
    pip.locate_submodules()
    pip.resolve_dependencies()

    print pip.dependencies

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

