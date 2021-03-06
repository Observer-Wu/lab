#coding:utf-8
import separate
import os
import filer
import math
import urllib2,urllib
emotion_count=5
feature_dict={}
#pre_list=[math.log(1.0/emotion_count)]*emotion_count
pre_list=[0.2,0.2,0.2,0.2,0.2]
pre_list=[math.log(pro) for pro in pre_list]

def load_feature(fpath):
    global feature_dict
    f_feature=file(fpath)
    for line in f_feature:
        line_arr=line.strip().split('\t')
        feature=line_arr[0]
        pre_pro_list=[float(pre_pro) for pre_pro in line_arr[1:]]
        feature_dict[feature]=pre_pro_list
    f_feature.close()

#load_feature('5emotion_cla/words_pre_pro.last')
load_feature(os.path.join(os.getcwd(), 'lib', 'words_pre_pro.last'))
#输入为utf8格式的经分词处理后的字符串数组
def classify(seg):
    word_list=[word for word in seg if word and not word=='#']
    if len(word_list)<5:
        return -1
    emotion_list=list(pre_list)
    is_true=False
    for word in word_list:
        try:
            pre_pro_list=feature_dict[word]
            is_true=True
            for emotion in range(emotion_count):
                try:
                    emotion_list[emotion]+=math.log(pre_pro_list[emotion])
                except ValueError:
                    raise
        except KeyError:
            pass
    if not is_true:
        return -1
    max_emotion=0
    for emotion in range(emotion_count):
        if emotion_list[emotion]!=0 and emotion_list[emotion]>emotion_list[max_emotion]:
            max_emotion=emotion
    return max_emotion
if __name__=='__main__':
    s = "心里有事就睡不好，乱乱乱。。。[可怜] http://t.cn/RZTncpi"
    s = filer.filter(s)
    print s
    seg = separate.separate(s)
    print '\t'.join(seg)
    print classify(seg)
