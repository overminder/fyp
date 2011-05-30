
import urlparse # for urljoin
import re # for url matching
import sys # for printing...

#from twisted.internet import epollreactor
#epollreactor.install() # epoll is fast
from twisted.internet import reactor, defer
from twisted.web import client
from twisted.python import util
from enc_getpage import get_page

from BeautifulSoup import BeautifulSoup
from soupselect import select as css_sel


def select_hrefs(parser, url_matcher, page_html, base_url):
    """select hrefs from the given page text
    @returns: a list of hrefs"""
    urls = parser(page_html, 'a', href=True)
    res = []
    for url in urls:
        if not url.startswith('http'):
            res.append(urlparse.urljoin(base_url, url))
        else:
            res.append(url)
    return filter(lambda s: url_matcher.search(s), res)


class SpiderIsFull(Exception):
    pass

class PageSpider(object):
    def __init__(self, url_matcher, max_num=10):
        self.to_visit = set()
        self.visited = {}
        self.max_num = max_num
        self.url_matcher = re.compile(url_matcher)
        self.count = 0

    def get_crawled(self):
        res = {}
        for k, v in self.visited.iteritems():
            if v != 'Dummy':
                res[k] = v
        return res

    def give_job(self):
        url = self.to_visit.pop()
        self.visited[url] = 'Dummy'
        return url

    def give_all_jobs(self):
        to_ret = []
        while self.to_visit:
            to_ret.append(self.give_job())
        return to_ret

    def add_page(self, url, page_text):
        self.count += 1
        self.visited[url] = page_text

        new_hrefs = select_hrefs(self.parser, self.url_matcher, page_text, url)
        for new_href in new_hrefs:
            if new_href not in self.visited:
                self.to_visit.add(new_href)

        if self.page_count() > self.max_num:
            raise SpiderIsFull('[%d / %d]' % (self.page_count(), self.max_num))

    def fail_page(self, url):
        del self.visited[url] # set it to be unvisited

    def page_count(self):
        return self.count

    def dump_to(self, fname, full_dump=False):
        import json
        with open(fname, 'w') as f:
            if full_dump:
                json.dump(self.visited, f, indent=4)
            else:
                json.dump(self.visited.keys(), f, indent=4)


def crawl_pages(start_page, url_matcher, encoding, timeout, max_num, parser):
    pages_d = defer.Deferred()
    spider = PageSpider(url_matcher, max_num)
    spider.parser = parser

    def on_err(errobj):
        evalue = errobj.value
        if isinstance(evalue, tuple) and len(evalue) == 2:
            url, reason = evalue
            spider.fail_page(url)

    defer_fired = []
    def page_recvd((url, text)):
        try:
            spider.add_page(url, text)
        except SpiderIsFull:
            if not defer_fired:
                defer_fired.append(None)
                pages_d.callback(spider.get_crawled())
            return

        urls = spider.give_all_jobs()

        # draw a point
        sys.stdout.write('.')
        sys.stdout.flush()

        for url in urls:
            next_d = get_page(str(url), enc=encoding, timeout=timeout)
            next_d.addCallback(page_recvd)
            next_d.addErrback(on_err)

    # initial crawl
    d = get_page(start_page, enc=encoding, timeout=timeout, must_succ=True)
    d.addCallback(page_recvd)
    d.addErrback(on_err)

    return pages_d # defer that will callback with pages


if __name__ == '__main__':
    from policyrunner import make_parse_engines
    crawl_pages(
        start_page='http://news.sina.com.hk',
        url_matcher=r'http://news.sina.com.hk',
        encoding='big5',
        timeout=10,
        max_num=10,
        parser=make_parse_engines()['pyquery']
    ).addCallback(lambda v: (util.println(v), reactor.stop()))
    reactor.run()

