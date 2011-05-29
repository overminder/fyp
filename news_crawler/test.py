"""
test each modules by fetching several pages and pretty-print them out
"""

import traceback
from twisted.internet import reactor

MAX_LEN = 33
KEYS = [u'url', u'time', u'title', u'body', u'timestamp']

def pretty_print(arti):
    print
    for key in KEYS:
        val = unicode(arti[key])
        if len(val) > MAX_LEN and key in [u'title', u'body']:
            print u'(%s => %s...)' % (key, val[:MAX_LEN])
        else:
            print u'(%s => %s)' % (key, val)

def test_module(module_name):
    mod = __import__(module_name)

    def pprint_all(founds):
        map(pretty_print, founds)

    mod.run(10).addCallback(pprint_all)

if __name__ == '__main__':
    all_mod = ['qq']
    for mod in all_mod:
        test_module(mod)

    reactor.run()


