# -*- coding: utf-8 -*-

import ctypes
import atexit
import os
from matplotlib import *
from nltk import FreqDist

curr = os.getcwd()
filepath = os.path.dirname(os.path.abspath(__file__))
os.chdir(filepath)
ictclas_lib = ctypes.CDLL(os.path.join(filepath, 'test.so'))

ictclas_lib.do_init()
atexit.register(ictclas_lib.do_finalize)
do_paragraph = ictclas_lib.do_paragraph
os.chdir(curr)

def segmentate(sentence):
    return paragraph(ctypes.c_char_p(do_paragraph(sentence, len(sentence))).value)


tagLabel = [
    ["n",["nr","ns","nt","nz","nl","ng"]],
    ["t",["tg"]],
    ["s"],
    ["f"],
    ["v",["vd","vn","vshi","vyou","vf","vx","vi","vl","vg"]],
    ["a",["ad","an","ag","al"]],
    ["b",["bl"]],
    ["z"],
    ["r",["rr",["rz",["rzt","rzs","rzv"],["ry",["ryt","rys","ryv"]],"rg"]]],
    ["m",["mq"]],
    ["q",["qv","qt"]],
    ["d"],
    ["p",["pba","pbei"]],
    ["c",["cc"]],
    ["u",["uzhe","ule","uguo","ude1","ude2","ude3","usuo","udeng","uyy","udh","uls","uzhi","ulian"]],
    ["e"],
    ["y"],
    ["o"],
    ["h"],
    ["k"],
    ["x",["xx","xu"]],
    ["w"]
]


class paragraph():
    def __init__(self,string):
        """
           variable declaration 
        """
        #the body of the paragraph
        self.body = string         

        #the body of the paragrah as an array
        self.pairs = self.body.split(' ')

        #split body to two parts and get frequency distribution
        self.pair_word = []
        self.pair_type = []
        for pair in self.pairs:
            if len(pair.split('/'))>=2:
                self.pair_word.append(pair.split('/')[0])
                self.pair_type.append(pair.split('/')[1])

        self.word_fq = FreqDist(self.pair_word)
        self.type_fq = FreqDist(self.pair_type)

    def getTypeCount(self,outTag):
        return self.type_fq[outTag]

    def getWordCount(self,outTag):
        return self.word_fq[outTag]

if __name__ == '__main__':
    print segmentate("哈哈你是张逸驰吗？").body

