from SPARQLWrapper import SPARQLWrapper 
from SPARQLWrapper import XML, GET, POST, JSON, JSONLD, N3, TURTLE, RDF
from SPARQLWrapper import SELECT, INSERT, DELETE
from SPARQLWrapper import URLENCODED, POSTDIRECTLY 
from SPARQLWrapper.Wrapper import QueryResult, QueryBadFormed, EndPointNotFound, EndPointInternalError

import string
import math
import xmltodict, json
import string

inputFile = open('edgefile.txt', 'r')

vector_q = SPARQLWrapper('http://localhost:8080/openrdf-workbench/repositories/vector/query')
vector_u = SPARQLWrapper('http://localhost:8080/openrdf-workbench/repositories/vector/update')
edges_q = SPARQLWrapper('http://localhost:8080/openrdf-workbench/repositories/edges/query')
edges_u = SPARQLWrapper('http://localhost:8080/openrdf-workbench/repositories/edges/update')
# for populating the graph (to be used only once)
def populate():
    for line in inputFile: 
        record = string.split(line, " ")
        src = record[0].rstrip()
        dst = record[1].rstrip()
        vector_u.setMethod(POST)
        edges_u.setMethod(POST)

        edges_u.setQuery('PREFIX vert:<http://mygraph.org/vertex/> \
                         PREFIX link:<http://mygraph.org/linkedto> \
                         INSERT DATA {vert:'+src+' link: vert:'+dst+'}')
        edges_u.query()

        vector_u.setQuery('PREFIX vert:<http://mygraph.org/vertex/> \
                         PREFIX score:<http://mygraph.org/score> \
                         INSERT DATA {vert:'+src+' score: \"0.001\"}')
        vector_u.query()

        
#populate() 
#def update():

def query():
    sparql.setMethod(GET)
    sparql.setQuery('SELECT ?s ?p ?o {?s ?p ?o} ORDER BY ?s ?p')

    results = sparql.query().convert()

    s = results.toxml()
    obj = xmltodict.parse(s)
    json_input = json.dumps(obj) #this is a string
    decoded = json.loads(json_input) #this is a json object(?)
    #print json.dumps(obj,sort_keys=True,indent=4)

    for i in range (len(decoded['sparql']['results']['result'])):
        print decoded['sparql']['results']['result'][i]['binding'][0]['uri']['#text']
        edge = decoded['sparql']['results']['result'][i]['binding'][1]['uri']
        print edge

        if 'linkedto' in edge:
            print decoded['sparql']['results']['result'][i]['binding'][2]['uri']['#text']
        else:
            print decoded['sparql']['results']['result'][i]['binding'][2]['literal']

