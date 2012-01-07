#!/usr/bin/env python

import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.normpath(os.path.join(HERE, '../../')))
#
from pysource.api import parse_source, get_import_names, get_module_accessors

def main(argv):
    try:
        filename = argv[1]
    except IndexError:
        print 'usage: %s [filename]' % argv[0]
        return 1
    #
    with open(filename) as f:
        module_node = parse_source(f.read())
    import_names = list(get_import_names(module_node))
    accessors = list(get_module_accessors(module_node))
    print import_names
    print accessors

if __name__ == '__main__':
    main(sys.argv)

