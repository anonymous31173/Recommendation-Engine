import requests
import re
import json
entities=[]
headers={"content-type":"application/json"}
url="http://neo4j:rr@localhost:7474/db/data/index/node"
res=requests.get(url).json()
for i in res.keys():
	t=re.findall('[A-Z]{1}[a-zA-Z]+',i)
	if len(t)!=0:
		entities.append(t[0])
#print entities
url1="http://neo4j:rr@localhost:7474/db/data/cypher"
#for i in entities:
	##query="match (n:"+i+") return n.name"
	#d={"query":query}
	#resp=requests.post(url1,data=json.dumps(d),headers=headers).json()['data']
	#print resp
