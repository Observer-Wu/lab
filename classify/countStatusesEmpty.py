import time
import datetime
from pymongo import MongoClient

noStatuses = []
statusesNone = []
statusesZero = []
other = []
def map_count(user):
    if 'statuses' not in user:
        noStatuses.append(user['id'])
    elif user.get('statuses', None) is None:
        statusesNone.append(user['id'])
    elif len(user.get('statuses', [])) == 0:
        statusesZero.append(user['id'])
    else:
        other.append(user['id'])


maxt = datetime.datetime.strptime('Feb 01 00:00:00 2000', '%b %d %H:%M:%S %Y')
mint = datetime.datetime.strptime('Feb 01 00:00:00 2020', '%b %d %H:%M:%S %Y')
def count_time(user):
    if 'statuses' not in user or user.get('statuses', None) is None or len(user.get('statuses', [])) == 0:
        return
    def map_time(weibo):
        global maxt, mint
        weibo_t = datetime.datetime.strptime(weibo['created_at'], '%a %b %d %H:%M:%S +0800 %Y')
        maxt = weibo_t if weibo_t > maxt else maxt
        mint = weibo_t if weibo_t < mint else mint

    map(map_time, user['statuses'])


if __name__ == '__main__':
    db = MongoClient('10.2.14.188', 27777).weibo
    coll = db.zombie
    map(count_time, coll.find({}, {'id':1, 'statuses': []}))
    with open('/home/wujunran/classify/timeZombie', 'w') as fp:
        '''
        fp.write('%s no statuses: %d\n' %(time.strftime('%Y-%m-%d %H:%M:%S'), len(noStatuses)))
        fp.write('%s statuses is None: %d\n' %(time.strftime('%Y-%m-%d %H:%M:%S'), len(statusesNone)))
        fp.write('%s len of statuses is 0: %d\n' %(time.strftime('%Y-%m-%d %H:%M:%S'), len(statusesZero)))
        fp.write('%s len of others: %d\n' %(time.strftime('%Y-%m-%d %H:%M:%S'), len(other)))
        '''
        fp.write('max time:%s\n' % (maxt))
        fp.write('min time:%s' % (mint))



