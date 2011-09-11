import copy
from spider import crawl_pages
import time
from twisted.internet import reactor, defer

def make_parse_engines():
    engine_cache = {}
    def using_bsoup(page_html, selector, **kw):
        from BeautifulSoup import BeautifulSoup
        from soupselect import select as css_sel

        if page_html not in engine_cache:
            soup = BeautifulSoup(page_html)
            engine_cache[page_html] = soup
        else:
            soup = engine_cache[page_html]

        tags_got = css_sel(soup, selector)
        if kw.get('text'):
            return ''.join(map(lambda t: t.text, tags_got)).strip()
        if kw.get('href'):
            hrefs = []
            for tag in tags_got:
                try:
                    hrefs.append(tag['href'])
                except KeyError:
                    pass
            return hrefs
        # else
        return tags_got

    def using_pyquery(page_html, selector, **kw):
        from pyquery import PyQuery

        if page_html not in engine_cache:
            pq = PyQuery(page_html)
            engine_cache[page_html] = pq
        else:
            pq = engine_cache[page_html]

        tags_got = pq(selector)
        if kw.get('text'):
            txt = tags_got.text()
            if txt is None:
                return ''
            return txt.strip()

        if kw.get('href'):
            def get_href(tag):
                return tag.get('href')
            return filter(lambda item: item, map(get_href, tags_got))
        # else
        return tags_got

    def test(engine, url):
        import urllib
        s = urllib.urlopen(url).read()
        hrefs = engine(s, 'a', href=True)
        texts = engine(s, 'a', text=True)
        print 'hrefs len = %d' % len(hrefs)
        print 'first 10: %s' % hrefs[:10]
        print 'text len = %d' % len(texts)

    return {
        'BeautifulSoup': using_bsoup,
        'pyquery': using_pyquery,
        '_test': test,
    }


def run(policy, **kw):
    """
    @param policy: a CrawlPolicy object.
    @param kw: additional policies to override the default value
    @return: a defer object in the format of
    {url, titie, body, timestamp, publish_time}
    """
    d = defer.Deferred()
    founds = []
    policy = copy.copy(policy)
    policy.__dict__.update(kw) # overriding options

    parser = make_parse_engines()[policy.parse_engine]

    def _cb(pages):
        """callback for crawl_pages()"""
        for url, page in pages.iteritems():
            try:
                parse_article(page, url)
            except ValueError, err:
                print 'parsing error on %s -- reason: %s' % (url, err)
                continue
        d.callback(founds)

    def parse_article(page_got, page_url):
        """analyze one particular article"""
        title = parser(page_got, policy.title_selector, text=True)
        if not title: raise ValueError, 'no title'

        body = parser(page_got, policy.body_selector, text=True)
        if not body: raise ValueError, 'no body'

        pub_time = parser(page_got, policy.pubtime_selector, text=True)
        if not pub_time: raise ValueError, 'no time'

        founds.append({
            u'url': page_url,
            u'title': title,
            u'body': body,
            u'timestamp': time.time(), # floating epoch time
            u'time': pub_time,
        })

    crawl_pages(
        start_page=policy.site_url,
        url_matcher=policy.news_matcher,
        encoding=policy.encoding,
        timeout=policy.timeout,
        max_num=policy.max_num,
        parser=parser
    ).addCallback(_cb)

    return d

if __name__ == '__main__':
    # testing parse engines
    engines = make_parse_engines()
    pq = engines['pyquery']
    soup = engines['BeautifulSoup']

    tester = engines['_test'] 
    tester(pq, 'http://news.qq.com')
    #tester(soup, 'http://news.qq.com')

