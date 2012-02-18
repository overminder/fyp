import os
import time
import pytest
from pysource.graph.installer import uninstall_package
from pysource.graph.builder import GraphBuilder
from pysource.graph.viewer import Viewer

@pytest.mark.skipif('1')
def test_build_pip_deps():
    # pip is a downloaded module.
    builder = GraphBuilder('pip', max_num_nodes=10)
    builder.build()
    v = Viewer(builder)

    path = 'sample-graph.png'
    v.output_image(path)
    assert os.path.isfile(path)
    os.system('xdg-open %s' % path)

