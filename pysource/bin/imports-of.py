import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.normpath(os.path.join(HERE, '../../')))
#
from pysource.api import get_import_names

def main(argv):
    try:
        filename = argv[1]
    except IndexError:
        print 'usage: %s [filename]' % argv[0]
        return 1
    #
    with open(filename) as f:
        import_names = get_import_names(f.read())
    for name in import_names:
        print name

if __name__ == '__main__':
    main(sys.argv)

