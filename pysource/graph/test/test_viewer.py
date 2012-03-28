import os
import time
import pytest
from pysource.graph.space import Space
from pysource.graph.builder import GraphBuilder
from pysource.graph.viewer import Viewer

def test_build_pip_deps():
    # pip is a downloaded module.
    builder = GraphBuilder(Space(), ['pip', 'django'], max_num_package=50)
    builder.build()
    v = Viewer(builder.finished_packages)

    path = 'sample-graph.png'
    v.output_image(path)
    assert os.path.isfile(path)
    os.system('xdg-open %s' % path)

