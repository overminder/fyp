from pysource.graph.builder import GraphBuilder
from pysource.graph.space import Space

def test_build_pip_deps():
    builder = GraphBuilder(Space(), 'pip', max_num_package=50)
    builder.build()
    print builder.finished_packages # package-name -> package

