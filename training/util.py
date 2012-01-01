import os

def local_path(rel_path, base=__file__):
    """ Turn :relpath into an absolute path base on :base.
    """
    return os.path.join(os.path.dirname(os.path.abspath(base)), rel_path)

