"""better support for different locale
"""

from twisted.internet import reactor, defer
from twisted.web import client
from twisted.python import util
import traceback
import StringIO
import gzip

RETRY_THRESHOLD = 15

def get_page(url, enc=None, timeout=5, retry_interval=1, must_succ=False):
    d = defer.Deferred()
    page_d = client.getPage(url, agent='Mozilla/5.0 (X11; Linux x86_64)\
    AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.57 Safari/534.24',
    headers={
        'Referer': url,
    })

    retry_interval *= 2

    def _retry(reason):
        if retry_interval > RETRY_THRESHOLD:
            _errback('too many retries')
            return

        print 'fetching %s: retry after %s second, reason -- %s' % (
                url, retry_interval, reason)
        reactor.callLater(retry_interval, lambda: get_page(
                url, enc, timeout, retry_interval, must_succ).addCallback(
                        lambda cbval: d.callback(cbval)).addErrback(
                        lambda errobj: d.errback(errobj.value)))

    def _callback(text):
        if timeout_handler.active():
            timeout_handler.cancel()
        else:
            return # already fired this defer
        compressedstream = StringIO.StringIO(text)
        gzipper = gzip.GzipFile(fileobj=compressedstream) 
        data = gzipper.read()
        if enc:
            try:
                data = data.decode(enc)
            except UnicodeDecodeError: # fail to decode the page
                _retry('decode err')
                return
        print data
        d.callback((url, text))

    eb_called = []
    def _errback(reason):
        if not eb_called:
            if reason == 'timeout' and must_succ:
                _retry(reason)
                return
            eb_called.append(None) # make it true
            print 'error happens: %s' % reason
            d.errback((url, reason))

    timeout_handler = reactor.callLater(timeout, _errback, 'timeout')

    page_d.addCallback(_callback)
    page_d.addErrback(_errback)
    return d

def test():
    get_page('http://news.qq.com', 'gb2312', 10).addCallback(
            lambda cbv: (util.println(cbv[0],
                                      cbv[1][1500:2000].encode('utf-8')),
                reactor.stop())).addErrback(
            lambda cbv: (util.println(traceback.print_tb(cbv.tb), 
                                      cbv.value), reactor.stop()))

if __name__ == '__main__':
    test()
    reactor.run()


