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

sparql_q = SPARQLWrapper('http://localhost:8080/openrdf-workbench/repositories/eigen/query')
sparql_u = SPARQLWrapper('http://localhost:8080/openrdf-workbench/repositories/eigen/update')
# for populating the graph (to be used only once)
def populate():
    for line in inputFile: 
        record = string.split(line, " ")
        src = record[0].rstrip()
        dst = record[1].rstrip()
        sparql_u.setMethod(POST) 

        sparql_u.setQuery('PREFIX vert:<http://mygraph.org/vertex/> \
                         PREFIX link:<http://mygraph.org/linkedto> \
                         INSERT DATA {vert:'+src+' link: vert:'+dst+'}')
        sparql_u.query()

        sparql_u.setQuery('PREFIX vert:<http://mygraph.org/vertex/> \
                         PREFIX score:<http://mygraph.org/score> \
                         INSERT DATA {vert:'+src+' score: 0.001}')
        sparql_u.query()

#populate() 

def MVM():
    del_array = [] # array for storing values to delete
    ins_array = [] # array for storing values to insert

    sparql_q.setMethod(GET)
    sparql_q.setQuery('PREFIX score:<http://mygraph.org/score> \
                        SELECT ?s ?p ?o \
                        {?s ?p ?o . \
                         FILTER(?p = score:)} ')
    prev_scores = sparql_q.query().convert()
    s = prev_scores.toxml()
    obj = xmltodict.parse(s)
    json_input = json.dumps(obj) #this is a string
    decoded = json.loads(json_input) #this is a json object(?)
    #print json.dumps(obj,sort_keys=True,indent=4)

    # populates the array with the vector elements we need to delete later
    for i in range (len(decoded['sparql']['results']['result'])):
        nid = decoded['sparql']['results']['result'][i]['binding'][0]['uri']['#text']
        edge = decoded['sparql']['results']['result'][i]['binding'][1]['uri']
        score = decoded['sparql']['results']['result'][i]['binding'][2]['literal']['#text']
        elem = '<' + nid + '> <' + edge + '> ' + score
        del_array.append(elem)

    sparql_q.setQuery('PREFIX link:<http://mygraph.org/linkedto> \
                        PREFIX score:<http://mygraph.org/score> \
                        SELECT ?src (SUM(?score) AS ?totalScore) \
                        {?nid score: ?score . \
                        ?src link: ?dst . \
                        FILTER(?dst = ?nid) \
                        } GROUP BY ?src')

    new_scores = sparql_q.query().convert()
    vectorSum = 0
    s = new_scores.toxml()
    obj = xmltodict.parse(s)
    json_input = json.dumps(obj) #this is a string
    decoded = json.loads(json_input) #this is a json object(?)
    print json.dumps(obj,sort_keys=True,indent=4)

    for i in range (len(decoded['sparql']['results']['result'])):
        nid = decoded['sparql']['results']['result'][i]['binding'][1]['uri']['#text'] 
        score = decoded['sparql']['results']['result'][i]['binding'][0]['literal']['#text']
        edge = 'http://mygraph.org/score'
        elem = '<' + nid + '> <' + edge + '> ' + score
        ins_array.append(elem)
    

MVM()
