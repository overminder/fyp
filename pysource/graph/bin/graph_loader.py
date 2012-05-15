import os
import cPickle as pickle


INPUT_FILE = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'modules-graph.p')

def load_knowledge_graph():
    with open(INPUT_FILE) as f:
        return pickle.load(f)

