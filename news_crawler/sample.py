"""An sample news scrapping module, showing some must-have functions"""

from datetime import datetime
from hasher import hash_digest

target_url = u'http://www.foo.com'


def run(prev_found=None, max_num=10):
    """
    @param prev_found: a dict containing key-value pairs of (hash-of-url,
                       article) used to determine if we have duplicated news
    @param max_num: how many news should we scrap?
    @return: a dict of (hash-of-url, article)
    """
    if prev_found is None:
        prev_found = {}

    founds = [{
        u'url': u'http://www.qq.com/first',
        u'timestamp': datetime.now(),
        u'title': u'Hello world!',
        u'body': u'1234 ' * 50},
    {
        u'url': u'http://www.qq.com/second',
        u'timestamp': datetime.now(),
        u'title': u'Hello world!',
        u'body': u'1234 ' * 50
    }]

    res_gen = ((hash_digest(d[u'url']), d) for d in founds)
    return dict(res_gen)


def test():
    """test this module"""
    n_runs = 10
    print run(n_runs)

if __name__ == '__main__':
    test()

