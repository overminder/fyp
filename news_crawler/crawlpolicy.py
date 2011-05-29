
class CrawlPolicy(object):
    """for example..."""
    sitename = 'sohu'
    encoding = 'gbk'
    site_url = 'http://news.sohu.com'
    news_matcher = r'http://news.sohu.com/.+?\d+?\.shtml'
    max_num = 10
    timeout = 10
    title_selector = 'div#contentA h1'
    body_selector = 'div#contentA #contentText'
    pubtime_selector = 'div#contentA .sourceTime .r'

def make_policy(**kw):
    res = CrawlPolicy()
    for k, v in kw.iteritems():
        setattr(res, k, v)
    return res

all_policies = {
    'qq': make_policy(sitename='qq',
                      encoding='gbk',
                      site_url = 'http://www.qq.com',
                      news_matcher = r'http://news.qq.com/.+?\d+?\.htm',
                      max_num=10,
                      timeout=10,
                      title_selector='#C-Main-Article-QQ .hd h1',
                      body_selector='#Cnt-Main-Article-QQ p',
                      pubtime_selector='span.pubTime'),
    'sohu': make_policy(), # it's already sohu's
}

