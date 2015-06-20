import threading
import time
import requests
import json
import sys
headers={"content-type":"application/json"}
#count=0
url="http://localhost:7474/db/data/cypher"
def synchronized(func):
	
    func.__lock__ = threading.Lock()
	#before critical section
    def synced_func(*args, **kws):
    	#critical section
        with func.__lock__:
            return func(*args, **kws)

    return synced_func
class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
 
    def run(self):
        self._target(*self._args)
 
@synchronized
def search_with_lock(args):
	query={"query":args}
	return requests.post(url,data=json.dumps(query),headers=headers).json()['data']


if __name__=="__main__":
	query1="""start p=node:place('withinDistance:[28.6139,77.2090,30.0]') match p where p.name=~'.*(?i)"""+sys.argv[1]+""".*'
with collect (distinct p.name) as places,p.type as type
match (c:Class)-[r]-(c1:Class) where c.class=type
return collect( distinct c1.class) as classes,places,type"""
	query2="""match (n:Class)-[r:INHERITS]->(n1) where n.class=~'.*(?i)"""+sys.argv[1]+"""*.' 
with  collect( distinct n1.class) as ext,n
start p=node:place('withinDistance:[28.6138967, 77.2159562,10.0]') match (p)-[r1]-(c:Class) where c.class in ext or c.class=n.class with 
case c.class
when n.class
then collect (distinct p) 
else
collect (distinct p)  end  as result,p.type as types,c
return extract(n IN result| n.name) as names,extract(b in result|b.rating) as ratings,extract(c in result|c.phone) as contacts,types,c.delhi_randomness as randomness order by randomness;"""
	thread1=FuncThread(search_with_lock,query1)
	thread2=FuncThread(search_with_lock,query2)
	thread1.start()
	thread2.start()
	thread1.join()
	thread2.join()
