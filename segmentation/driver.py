#coding: utf-8

import ctypes
import atexit

h = ctypes.CDLL('./test.so')
h.do_init()

def run(sentence):
    return ctypes.c_char_p(h.do_paragraph(sentence, len(sentence))).value

atexit.register(h.do_finalize)

if __name__ == '__main__':
    print run('《中文》教材第一册')

