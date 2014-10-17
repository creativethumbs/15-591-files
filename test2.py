from SPARQLWrapper import SPARQLWrapper 
from SPARQLWrapper import XML, GET, POST, JSON, JSONLD, N3, TURTLE, RDF
from SPARQLWrapper import SELECT, INSERT
from SPARQLWrapper import URLENCODED, POSTDIRECTLY 
from SPARQLWrapper.Wrapper import QueryResult, QueryBadFormed, EndPointNotFound, EndPointInternalError
import xmltodict, json

sparql = SPARQLWrapper('http://localhost:8080/openrdf-workbench/repositories/test/update')
sparql2 = SPARQLWrapper('http://localhost:8080/openrdf-workbench/repositories/test2/update')
sparql3 = SPARQLWrapper('http://localhost:8080/openrdf-workbench/repositories/test/query')

'''
sparql.setMethod(POST)

x = '1'
y = '2'
z = '3'

sparql.setQuery('PREFIX e:<http://example.org/> INSERT DATA {e:'+x+' e:'+y+' e:'+z+'}')

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

print results

print
'''
sparql3.setMethod(GET)

sparql3.setQuery('SELECT ?s ?p ?o {?s ?p ?o}')

results = sparql3.query().convert()

s = results.toxml()
obj = xmltodict.parse(s)
json_input = json.dumps(obj) #this is a string
decoded = json.loads(json_input) #this is a json object(?)
#print json.dumps(obj,sort_keys=True,indent=4)

#this looks really bad but at least it works
for i in range (len(decoded['sparql']['results']['result'])):
    for j in range (len(decoded['sparql']['results']['result'][i]['binding'])):
        print decoded['sparql']['results']['result'][i]['binding'][j]['uri']['#text']



