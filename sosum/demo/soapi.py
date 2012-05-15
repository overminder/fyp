import re
from stackexchange import StackOverflow, Site
from pyquery import PyQuery as PQ

so = Site(StackOverflow)

def extract_post_id(url):
    pattern = r'(?:https?://)?stackoverflow.com/questions/(\d+?)/'
    match_obj = re.match(pattern, url)
    return match_obj.group(1)

def fetch_question(qid):
    return so.question(qid, body=True)

def convert_nonalpha(sentence):
    return ''.join(c if c.isalpha() else ' ' for c in sentence)

def process_question(q):
    body = PQ(q.body)
    bodywords = convert_nonalpha(body.text()).split()
    keywords = list(_exclude_stopwords(_exclude_nonmodules((set(bodywords)))))
    answers = []
    for ans in q.answers:
        answers.append(list(_extract_code_segment(ans.body)))
    return keywords, answers

def _extract_code_segment(htmltext):
    tree = PQ(htmltext)
    for node in tree('code'):
        yield node.text

def _exclude_stopwords(words):
    from django.utils.stopwords import stopwords
    for word in words:
        if word not in stopwords:
            yield word

def _exclude_nonmodules(words):
    for w in words:
        if len(w) <= 1:
            continue
        if w[0].islower():
            yield w

