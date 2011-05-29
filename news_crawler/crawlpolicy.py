
class CrawlPolicy(object):
    sitename = 'sohu'
    encoding = 'gbk'
    max_num = 10
    timeout = 10
    title_selector = 'div#contentA h1'
    body_selector = 'div#contentA #contentText'
    pubtime_selector = 'div#contentA .sourceTime .r'

