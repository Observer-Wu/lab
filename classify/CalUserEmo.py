#!/usr/bin/env python
# encoding: utf-8

import os
import datetime
import traceback
from pymongo import MongoClient
from lib import filer, separate, emo_cls

DAY = 24 * 60 * 60
re = {str(i):[0 for j in range(2100)] for i in range(-1, 5)}


def map_cal_weibo(weibo):
    try:
        start = datetime.datetime.strptime('Jan 01 00:00:00 2010', '%b %d %H:%M:%S %Y')
        end = datetime.datetime.strptime('Oct 01 00:00:00 2015', '%b %d %H:%M:%S %Y')
        weibo_t = datetime.datetime.strptime(weibo['created_at'], '%a %b %d %H:%M:%S +0800 %Y')
        if weibo_t < start or weibo_t > end:
            return
        re[str(emo_cls.classify(separate.separate(filer.filter(weibo['text']))))][int((weibo_t - start).total_seconds() / DAY)]+= 1
    except:
        traceback.print_exc()


def map_cal_user(user):
    if 'statuses' not in user or user.get('statuses', None) is None or len(user.get('statuses', [])) == 0:
        return
    map(map_cal_weibo, user.get('statuses', []))


def cal(ty = 'zombie'):
    db = MongoClient('10.2.14.188', 27777).weibo
    coll = db.zombie if ty == 'zombie' else db.normal
    #map_cal_user(coll.find_one({'id':1918632444}, {'id':1, 'statuses':[]}))
    map(map_cal_user, coll.find({}, {'id':1, 'statuses':[]}))


if __name__ == '__main__':
    cal()
    with open('/home/wujunran/classify/countEmotion', 'w') as fp:
        fp.write(str(re))
    for i in range(-1, 5):
        print re[str(i)]
