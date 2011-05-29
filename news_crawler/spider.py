
import urlparse # for urljoin
import re # for url matching

from twisted.internet import epollreactor
epollreactor.install() # epoll is fast
from twisted.internet import reactor, defer
from twisted.web import client
from enc_getpage import get_page

from BeautifulSoup import BeautifulSoup
from soupselect import select as css_sel


def select_hrefs(url_matcher, page_html, base_url):
    """select hrefs from the given page text
    @returns: a list of hrefs"""
    soup = BeautifulSoup(page_html)
    a_tags = css_sel(soup, 'a')

    res = []
    for tag in a_tags:
        try:
            url = tag['href']
        except:
            continue # no href.
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

        new_hrefs = select_hrefs(self.url_matcher, page_text, url)
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


def test():
    TIMEOUT = 10 # should be enough
    NUM_OF = 1000
    #PAGE_ENC = 'gbk'
    PAGE_ENC = None
    #start_page = 'http://news.qq.com'
    start_page = 'http://www.sina.com.hk'
    spider = PageSpider(r'http://news.sina.com.hk', NUM_OF)

    def on_err(errobj):
        evalue = errobj.value
        if isinstance(evalue, tuple) and len(evalue) == 2:
            url, reason = evalue
            spider.fail_page(url)
            #print 'page %s failed, reason: %s' % (url, reason)
        else:
            pass # unknown error

    def page_recvd((url, text)):
        print 'page %s recvd' % url
        try:
            spider.add_page(url, text)
        except SpiderIsFull:
            if reactor.running:
                reactor.stop()
                print 'done'
            return

        urls = spider.give_all_jobs()
        print 'current page count: %s' % spider.page_count()
        for url in urls:
            next_d = get_page(str(url), enc=PAGE_ENC, timeout=TIMEOUT)
            next_d.addCallback(page_recvd)
            next_d.addErrback(on_err)

    # initialize the fetch
    d = get_page(start_page, enc=PAGE_ENC, timeout=TIMEOUT, must_succ=True)
    d.addCallback(page_recvd)
    d.addErrback(on_err)

    reactor.run()
    spider.dump_to('spider_dump') # after fetch NUM_OF pages, save them to a
                                  # file.

if __name__ == '__main__':
    test()

