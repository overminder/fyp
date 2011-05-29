#coding: utf-8

from datetime import datetime
from urllib2 import urlopen
import re

from BeautifulSoup import BeautifulSoup
from soupselect import select as css_sel

from twisted.internet import reactor
from twisted.web.client import getPage


target_url = 'http://www.qq.com'
front_news = re.compile('http://news.qq.com/.+?\d+?\.htm')

def get_news_url(base_url, cb):
    getPage(base_url, 


def get_url_from_frontpage(page_html, cb):
    soup = BeautifulSoup(page_html)
    hrefs = 
    cb(front_news.findall(page_html))

def fetch_page(url, cb, **kw):
    print 'fetching %s' % url
    cb(urlopen(url).read(), **kw)

def run(max_num=10):
    founds = []

    def parse_article(page_got, page_url):
        page_got = page_got.decode('gbk')
        soup = BeautifulSoup(page_got)

        title = css_sel(soup, '#C-Main-Article-QQ .hd h1')
        if not title:
            raise ValueError, 'no title huh?'
        title = title[0].text

        body = css_sel(soup, '#Cnt-Main-Article-QQ p')
        if not body:
            raise ValueError, 'no body huh?'
        body = ''.join(map(lambda tag: tag.text, body))

        timestamp = css_sel(soup, 'span.pubTime')
        if not timestamp:
            raise ValueError, 'no timestamp huh?'
        timestamp = timestamp[0].text

        founds.append({
            u'url': page_url,
            u'title': title,
            u'body': body,
            u'timestamp': datetime.now(),
            u'time': timestamp
        })


    def handle_urls(urls):
        print 'got %d urls' % len(urls)
        for i, url in enumerate(urls):
            fetch_page(url, parse_article, page_url=url)
            if i > max_num:
                break

    get_url_from_frontpage(urlopen(target_url).read(), handle_urls)
    return founds


def test():
    print run()

if __name__ == '__main__':
    test()

