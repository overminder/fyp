from pyquery import PyQuery

def get_code_pieces(html_text):
    pq = PyQuery(html_text)
    return pq('code')
    