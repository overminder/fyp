#coding: utf-8

from spider import crawl_pages
from datetime import datetime
from BeautifulSoup import BeautifulSoup
from soupselect import select as css_sel
from twisted.internet import reactor, defer

target_url = 'http://news.sohu.com'
front_news = r'http://news.sohu.com/.+?\d+?\.shtml'

def run(max_num=10):
    """@returns: deferred object with a list of pages being found as
    callback"""
    d = defer.Deferred()
    founds = []

    def _cb(pages):
        """callback for crawl_pages()"""
        for url, page in pages.iteritems():
            try:
                parse_article(page, url)
            except ValueError, err:
                print url, err
                continue
        d.callback(founds)

    def parse_article(page_got, page_url):
        """analyze one particular article"""
        soup = BeautifulSoup(page_got)

        title = css_sel(soup, 'div#contentA h1')
        if not title:
            raise ValueError, 'no title huh?'
        title = title[0].text

        body = css_sel(soup, 'div#contentA #contentText')
        if not body:
            raise ValueError, 'no body huh?'
        body = ''.join(map(lambda tag: tag.text, body))

        pub_time = css_sel(soup, 'div#contentA .sourceTime .r')
        if not pub_time:
            raise ValueError, 'no publish time huh?'
        pub_time = pub_time[0].text

        founds.append({
            u'url': page_url,
            u'title': title,
            u'body': body,
            u'timestamp': datetime.now(),
            u'time': pub_time,
        })

    crawl_pages(
        start_page=target_url,
        url_matcher=front_news,
        encoding='gbk',
        timeout=10,
        max_num=10
    ).addCallback(_cb)

    return d

if __name__ == '__main__':
    import test
    test.test_module('sohu')
    reactor.run()

