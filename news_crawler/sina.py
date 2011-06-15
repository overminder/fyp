from datetime import datetime
from hasher import hash_digest
import sys
import urllib2
import urlparse
from BeautifulSoup import BeautifulSoup as BS
from soupselect import select

target_url = u'http://www.sina.com.cn'

   
def run(prev_found=None, max_num=100):
    """
    @param prev_found: a dict containing key-value pairs of (hash-of-url,
                       article) used to determine if we have duplicated news
    @param max_num: how many news should we scrap?
    @return: a dict of (hash-of-url, article)
    """
    if prev_found is None:
        prev_found = {}

    num = [0]
    founds = [{
        u'url': u'http://www.qq.com/sample',
        u'timestamp': datetime.now(),
        u'title': u'sampleTitle',
        u'body': u'sampleBody'},
    ]

    def get_content(url,num):
        if num[0] >= max_num:
            return
        response = urllib2.urlopen(url)
        msg = response.read()
        soup = BS(''.join(msg))
        
        news_body = select(soup,'div.blkContainerSblk')
        if len(news_body) == 1:
            num[0] = num[0] + 1
            title = select(soup,'h1#artibodyTitle')
            time = select(soup,'span#pub_date')
            content = select(soup,'div#artibody.blkContainerSblkCon')
            founds.append({
                u'url' : url,
                u'timestamp' 
            })


        links = select(soup, 'a')['href']
        for link in links:
            if link.find("news.sina.com.cn") != -1:
            get_content(url,num)
    get_content(target_url, num)            

    #res_gen = ((hash_digest(d[u'url']), d) for d in founds)
    #return dict(res_gen)


def test():
    """test this module"""
    n_runs = 10
    print run(n_runs)

if __name__ == '__main__':
    test()

