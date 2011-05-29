"""
test each modules by fetching several pages and pretty-print them out
"""

import traceback
from twisted.internet import reactor
import crawlpolicy
import policyrunner

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

def pprint_all(founds):
    map(pretty_print, founds)

def test_module(module_name):
    mod = __import__(module_name)
    mod.run(10).addCallback(pprint_all)

def test_policy(sitename):
    policyrunner.run(
        crawlpolicy.all_policies[sitename]).addCallback(pprint_all)

if __name__ == '__main__':
    sitenames = crawlpolicy.all_policies.keys()
    for sitename in sitenames:
        test_policy(sitename)
    reactor.run()


