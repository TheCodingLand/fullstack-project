
    
import redis
from operator import itemgetter
import time
import pytz
from datetime import datetime
from operator import itemgetter
from eventmanager import services


r = redis.StrictRedis(host='redis', decode_responses=True, port=6379, db=2)


def getAddedCalls():
    for key in r.scan_iter(match='*'):     
        try:
            c = r.hgetall(key)
        except redis.exceptions.ResponseError:
            pass
        s = services.Services(c)
        if s.done== True:
            r.delete(key)
            
#quick cleaup as this key is only used for real time data            



print("waiting for key to fill redis db")
time.sleep(15)

print ("Clearing Backlog")


keyhashes = []
keys = r.keys()    
#print (keys)
for key in keys:
    try:    
        k = r.hgetall(key)
        k['key']=key
        keyhashes.append(k)
    except:
        key.delete()

newlist = sorted(keyhashes, key=itemgetter('timestamp')) 
for item in newlist:
    #print(item['timestamp'])
    s = services.Services(item)
    if s.done== True:
        r.delete(item['key'])

print("Normal Loop")
while True:

    getAddedCalls()
    

        