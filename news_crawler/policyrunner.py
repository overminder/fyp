
import copy
from spider import crawl_pages
from datetime import datetime
from BeautifulSoup import BeautifulSoup
from soupselect import select as css_sel
from twisted.internet import reactor, defer

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

        title = css_sel(soup, policy.title_selector)
        if not title:
            raise ValueError, 'no title huh?'
        title = title[0].text

        body = css_sel(soup, policy.body_selector)
        if not body:
            raise ValueError, 'no body huh?'
        body = ''.join(map(lambda tag: tag.text, body))

        pub_time = css_sel(soup, policy.pubtime_selector)
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
        start_page=policy.site_url,
        url_matcher=policy.news_matcher,
        encoding=policy.encoding,
        timeout=policy.timeout,
        max_num=policy.max_num
    ).addCallback(_cb)

    return d


