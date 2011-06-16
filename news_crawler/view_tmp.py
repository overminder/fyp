#coding: utf-8
import json
import sys
sys.path.append('/home/paul/Documents/FYTproject/segmentation')
import segLib
d = json.load(open('qq.out'))[0]['body']
para =  segLib.segmentate(d.encode("utf-8"))
print para.body
