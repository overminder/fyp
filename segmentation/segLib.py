# -*- coding: utf-8 -*-

def segmentate(sentence):
    import os
    f = open("temp.txt","wb")
    f.write(sentence)
    f.close()
    outfile = "temp_result.txt"
    os.system("touch "+outfile)
    os.system("./test temp.txt "+outfile)
    f = open(outfile,'rb')
    s = f.read()
    os.system("rm temp.txt "+outfile)
    return s


#print segmentate("哈哈你是张逸驰吗？")

