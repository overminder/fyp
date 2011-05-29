
import traceback

MAX_LEN = 20
KEYS = [u'url', u'time', u'title', u'body', u'timestamp']

def pretty_print(arti):
    for key in KEYS:
        val = unicode(arti[key])
        if len(val) > MAX_LEN:
            print u'(%s, %s...)' % (key, val[:MAX_LEN])
        else:
            print u'(%s, %s)' % (key, val)

def test_module(module_name):
    mod = __import__(module_name)
    try:
        founds = mod.run(10)
        map(pretty_print, founds)
    except Exception, err:
        print 'module %s failed. reason:' % module_name
        traceback.print_exc()

if __name__ == '__main__':
    all_mod = ['qq']
    for mod in all_mod:
        test_module(mod)

