# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

import soapi
import graphapi

def index(req):
    return render_to_response('demo/index.html', {
            
        }, context_instance=RequestContext(req)
    )

def summarize(req):
    url = req.GET.get('url')
    post_id = soapi.extract_post_id(url)
    q = soapi.fetch_question(post_id)
    keywords, answers = soapi.process_question(q)
    kwgraph = graphapi.gen_subgraph_from_keywords(keywords)
    ansgraphs = [(graphapi.gen_subgraph_from_code(code), nth_ans, nth_code)
                 for nth_ans, codes in enumerate(answers)
                 for nth_code, code in enumerate(codes)]
    scores = [(graphapi.subgraph_distance(kwgraph, subgraph), nth_ans, nth_code)
              for (subgraph, nth_ans, nth_code) in ansgraphs]

    ans_score_sum = [0.0] * len(answers)
    for score, nth_ans, nth_code in scores:
        ans_score_sum[nth_ans] += score
    for i, score in enumerate(ans_score_sum):
        if len(answers[i]):
            ans_score_sum[i] = (i, score / len(answers[i]))
        else:
            ans_score_sum[i] = (i, 0)

    ans_score_sum.sort(key=lambda x: x[1], reverse=True)
    sorted_answers = [q.answers[i] for i, _ in ans_score_sum]

    return render_to_response('demo/summarization.html', {
            'url': url,
            'q': q,
            'sorted_answers': sorted_answers,
        }, context_instance=RequestContext(req)
    )

