from SPARQLWrapper import SPARQLWrapper 
from SPARQLWrapper import XML, GET, POST, JSON, JSONLD, N3, TURTLE, RDF
from SPARQLWrapper import SELECT, INSERT
from SPARQLWrapper import URLENCODED, POSTDIRECTLY 
from SPARQLWrapper.Wrapper import QueryResult, QueryBadFormed, EndPointNotFound, EndPointInternalError

import string
import math
import xmltodict, json
import string

inputFile = open('edgefile.txt', 'r')

sparql = SPARQLWrapper('http://localhost:8080/openrdf-workbench/repositories/eigen/query')
sparul = SPARQLWrapper('http://localhost:8080/openrdf-workbench/repositories/eigen/update')
# for populating the graph (to be used only once)
def populate():
    for line in inputFile: 
        record = string.split(line, " ")
        src = record[0].rstrip()
        dst = record[1].rstrip()

        sparul.setMethod(POST)
        sparul.setQuery('PREFIX vert:<http://mygraph.org/vertex/> \
                         PREFIX link:<http://mygraph.org/linkedto> \
                         PREFIX val:<http://mygraph.org/value> \
                         INSERT DATA {vert:'+src+' link: vert:'+dst+'}')
        sparul.query()

        sparul.setQuery('PREFIX vert:<http://mygraph.org/vertex/> \
                         PREFIX link:<http://mygraph.org/linkedto> \
                         PREFIX val:<http://mygraph.org/value> \
                         INSERT DATA {vert:'+src+' val: \"0.001\"}')
        sparul.query()
        
#populate()

def update():

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

