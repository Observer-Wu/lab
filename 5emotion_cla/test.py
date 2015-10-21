#coding:utf-8
import separate
import filer
import emo_cls
str = '恐惧恐惧恐惧恐惧恐惧恐惧恐惧'
str = filer.filter(str)
seg = separate.separate(str)
print emo_cls.classify(seg)
