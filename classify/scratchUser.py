#/usr/local/bin/python
#-*- coding:utf-8 -*-

import os
import logging
import requests
import traceback
import itertools
import subprocess
from pymongo import MongoClient
from logging.handlers import RotatingFileHandler

#set log
fh = RotatingFileHandler('/home/wujunran/classify/scratchZombieWeiboLog', maxBytes=10*1024*1024, backupCount=10)
fm = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
fh.setFormatter(fm)
logger = logging.getLogger('scratch')
logger.setLevel(logging.INFO)
logger.addHandler(fh)

DIC = '/home/wujunran/classify/'

class scratchUser:
    def __init__(self):
        db = MongoClient('10.2.14.188', 27777).weibo
        self.zombie = db.zombie
        self.normal = db.normal
        self.api_fans = 'http://118.244.212.186/queryFriends?uid=%s&userType=2&count=1000&page=0'
        self.api_info = 'http://118.244.212.186/queryWeiboUsers?uid=%s'
        self.api_weibo = 'http://118.244.212.186/queryUserWeibo?uid=%d&count=100&page=%d'


    def scratch_zombie_uid(self):
        def map_seed(uid):
            try:
                r = requests.get(self.api_fans % (uid))
                if r.status_code != 200:
                    return []
                logger.info('%s %d', uid, len(r.json()['ids']))
                return r.json()['ids']
            except:
                logger.error('Error:%s', uid)
                logger.error(traceback.format_exc())
                return []

        with open('/home/wujunran/classify/bigV') as fp:
                bigV = fp.read().split()
        zombie = list(itertools.chain.from_iterable(map(map_seed, bigV)))
        logger.info('zombie count:%d', len(zombie))
        with open('/home/wujunran/classify/zombie', 'w') as fp:
            fp.write(str(zombie[0]))
            for z in zombie[1:]:
                fp.write('\n%d' %(z))

    def scratch_user_info(self, ty):
        coll = self.zombie if ty == 'zombie' else self.normal
        def map_scratch_info(uid):
            try:
                r = requests.get(self.api_info % (uid))
                if r.status_code != 200 or 'errno' in r.json():
                    return
                coll.update({'id': r.json()['id']}, r.json(), upsert=True)
                logger.info('%s %s', ty, uid)
            except:
                logger.error('Error in %s', uid)
                logger.error(traceback.format_exc())

        with open(os.path.join(DIC, ty)) as fp:
            uids = fp.read().split()
        map(map_scratch_info, uids)

    def scratch_user_weibo(self, ty):
        coll = self.zombie if ty == 'zombie' else self.normal
        def check_running():
            if int(subprocess.check_output('ps -ef|grep scratchUser.py|grep -v grep|wc -l', shell=True))>1:
                return True
            return False

        def load_user():
            with open(os.path.join(DIC, ty)) as fp:
                return [{'id':int(line.split()[0]), 'statuses_count':int(line.split()[1])} for line in fp.read().split('\n') if len(line) > 0]

        def map_scratch_weibo(user):
            statuses = []
            try:
                for page in range(1, min(11, user['statuses_count']/100+2)):
                    r = requests.get(self.api_weibo % (user['id'], page), timeout=60)
                    if r.status_code != 200 or 'errno' in r.json():
                        break
                    statuses.extend(r.json().get('statuses', []))
            except:
                logger.error('%d\n%s', user['id'], traceback.format_exc())
            finally:
                try:
                    msg = '%d-%d-%d' % (user['id'], user['statuses_count'], len(statuses))
                    if len(statuses) == 0 and 'errno' in r.json():
                        msg = '%s--errno:%d' % (msg, r.json().get('errno', -1))
                    logger.info(msg)
                    coll.update({'id': user['id']}, {'$set': {'statuses': statuses}})
                except:
                    traceback.print_exc()

        if check_running():
            return
        with open(os.path.join(DIC, 'count')) as fp:
            index = int(fp.read())
        map(map_scratch_weibo, load_user()[index:index+1000])
        with open(os.path.join(DIC, 'count'), 'w') as fp:
            fp.write(str(index+1000))


if __name__ == '__main__':
    sc = scratchUser()
    sc.scratch_user_weibo('zombie')
