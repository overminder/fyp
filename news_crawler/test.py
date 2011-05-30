"""
test each modules by fetching several pages and pretty-print them out
"""

import json
import sys
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
            print u'(%s => %s ### %s)' % (key, val[:MAX_LEN], val[-MAX_LEN:])
        else:
            print u'(%s => %s)' % (key, val)

def pprint_all(founds):
    map(pretty_print, founds)
    return founds

def test_policy(sitename, **kw):
    def dump_to_file(founds):
        with open (sitename + '.out', 'w') as f:
            json.dump(founds, f, indent=4)
    policyrunner.run(
        crawlpolicy.all_policies[sitename], **kw).addCallback(
                pprint_all).addCallback(dump_to_file)


if __name__ == '__main__':
    if len(sys.argv) > 1: # testing given sites
        sitenames = sys.argv[1:]
    else: # all sites
        sitenames = crawlpolicy.all_policies.keys()

    for sitename in sitenames:
        print 'testing %s' % sitename
        test_policy(sitename, max_num=5)

    reactor.run()


