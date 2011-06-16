# -*- coding: utf-8 -*-

import ctypes
import atexit
import os

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
        self.body = string #the body of the paragraph
        self.pairs = self.body.split(' ')
        self.nounCount = 0
        self.verbCount = 0
        self.adjCount = 0
        self.pronCount = 0
        self.timeCount = 0
        for pair in self.pairs:
            if len(pair.split('/'))>=2:
                word = pair.split('/')[0]
                tag = pair.split('/')[1]
                if tag[:1] == 'n':
                    self.nounCount = self.nounCount + 1
                elif tag[:1] == 'v':
                    self.verbCount = self.verbCount + 1
                elif tag[:1] == 'a':
                    self.adjCount = self.adjCount + 1
                elif tag[:1] == 'r':
                    self.pronCount = self.pronCount + 1
                elif tag[:1] == 't':
                    self.timeCount = self.timeCount + 1
    def getCount(self,outTag):
        counter = 0
        for pair in self.pairs:
            if len(pair.split('/'))>=2:
                word = pair.split('/')[0]
                tag = pair.split('/')[1]
                if tag == outTag:
                    counter = counter + 1
        return counter

if __name__ == '__main__':
    print segmentate("哈哈你是张逸驰吗？").body

