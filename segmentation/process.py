# -*- coding: utf-8 -*-
from segLib import *

string = "曾派调查小组赴当地调查的世界基督教联合会15日呼吁包括联合国在内的国际社会，关注缅甸局势，倡议印度、中国等邻国为缅甸难民提供保护。该联合会同时敦促缅甸冲突双方停火，通过对话解决问题，结束长达数十年的国内武装冲突，减少人民的痛苦。与此同时，各国媒体纷纷发表评论称，缅甸需要的是对话，不是战争。"
print string
seg = segmentate(string)
print seg.body
print "Number of noun: %d" % seg.nounCount
print "Number of verb: %d" % seg.verbCount
print "Number of adjective: %d" % seg.adjCount
print "Number of pronoun: %d" % seg.pronCount
print "Number of time indicator: %d" % seg.timeCount



