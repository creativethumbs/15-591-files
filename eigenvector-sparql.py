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
outputFile = open('eigenvector.txt', 'w')
output_array = [] # array for writing to output text file

sparql_q = SPARQLWrapper('http://localhost:8080/openrdf-workbench/repositories/eigen/query')
sparql_u = SPARQLWrapper('http://localhost:8080/openrdf-workbench/repositories/eigen/update')
# for populating the graph (to be used only once)
def cleardata():
    # need to insert a 'dummy' element because if you tried to clear an empty
    # database, there will be errors
    sparql_u.setMethod(POST) 
    sparql_u.setQuery('PREFIX vert:<http://mygraph.org/vertex/> \
                     PREFIX link:<http://mygraph.org/linkedto> \
                     INSERT DATA {vert:0 link: vert:1}')
    sparql_u.query()
    sparql_u.setQuery('PREFIX vert:<http://mygraph.org/vertex/> \
                         PREFIX score:<http://mygraph.org/score> \
                         INSERT DATA {vert:0 score: 0.000}')
    sparql_u.query()

    del_vectors = [] 
    del_edges = [] 

    sparql_q.setMethod(GET)
    sparql_q.setQuery('PREFIX score:<http://mygraph.org/score> \
                        SELECT ?s ?o \
                        {?s score: ?o } ')
    allvectors = sparql_q.query().convert()
    s = allvectors.toxml()
    obj = xmltodict.parse(s)
    json_input = json.dumps(obj)
    decoded = json.loads(json_input) 

    if (len(decoded['sparql']['results']['result']) == 1):
        nid = decoded['sparql']['results']['result']['binding'][0]['uri']['#text']
        edge = 'http://mygraph.org/score'
        score = decoded['sparql']['results']['result']['binding'][1]['literal']['#text']
        elem = '<' + nid + '> <' + edge + '> ' + score
        del_vectors.append(elem)
    else:
        # populates the array with the vector elements we need to delete later
        for i in range (len(decoded['sparql']['results']['result'])):
            nid = decoded['sparql']['results']['result'][i]['binding'][0]['uri']['#text']
            edge = 'http://mygraph.org/score'
            score = decoded['sparql']['results']['result'][i]['binding'][1]['literal']['#text']
            elem = '<' + nid + '> <' + edge + '> ' + score
            del_vectors.append(elem)

    sparql_q.setMethod(GET)
    sparql_q.setQuery('PREFIX link:<http://mygraph.org/linkedto> \
                        SELECT ?s ?o \
                        {?s link: ?o } ')
    alledges = sparql_q.query().convert()
    s = alledges.toxml()
    obj = xmltodict.parse(s)
    json_input = json.dumps(obj) 
    decoded = json.loads(json_input)  

    if (len(decoded['sparql']['results']['result']) == 1):
        src = decoded['sparql']['results']['result']['binding'][0]['uri']['#text']
        edge = 'http://mygraph.org/linkedto'
        dst = decoded['sparql']['results']['result']['binding'][1]['uri']['#text']
        elem = '<' + src + '> <' + edge + '> <' + dst +'>'
        del_edges.append(elem)

    else:
        # populates the array with the vector elements we need to delete later
        for i in range (len(decoded['sparql']['results']['result'])):
            src = decoded['sparql']['results']['result'][i]['binding'][0]['uri']['#text']
            edge = 'http://mygraph.org/linkedto'
            dst = decoded['sparql']['results']['result'][i]['binding'][1]['uri']['#text']
            elem = '<' + src + '> <' + edge + '> <' + dst +'>'
            del_edges.append(elem)

    for item in del_vectors:
        sparql_u.setMethod(POST) 
        sparql_u.setQuery('DELETE DATA {'+item+'}')
        sparql_u.query()
    for item in del_edges:
        sparql_u.setMethod(POST) 
        sparql_u.setQuery('DELETE DATA {'+item+'}')
        sparql_u.query()

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

def MVM(iterNo):
    del_array = [] # array for storing values to delete
    ins_array = [] # array for storing values to insert
    vectorSum = 0

    sparql_q.setMethod(GET)
    sparql_q.setQuery('PREFIX score:<http://mygraph.org/score> \
                        SELECT ?s ?p ?o \
                        {?s ?p ?o . \
                         FILTER(?p = score:)} ')
    prev_scores = sparql_q.query().convert()
    s = prev_scores.toxml()
    obj = xmltodict.parse(s)
    json_input = json.dumps(obj) 
    decoded = json.loads(json_input) 

    # populates the array with the vector elements we need to delete later
    for i in range (len(decoded['sparql']['results']['result'])):
        nid = decoded['sparql']['results']['result'][i]['binding'][0]['uri']['#text']
        edge = decoded['sparql']['results']['result'][i]['binding'][1]['uri']
        score = decoded['sparql']['results']['result'][i]['binding'][2]['literal']['#text']
        elem1 = '<' + nid + '> <' + edge + '> ' + score 
        del_array.append(elem1) 

        if (iterNo == 2):
            output_array.append('<'+nid+'>, 1, 0.001')

    sparql_q.setQuery('PREFIX link:<http://mygraph.org/linkedto> \
                        PREFIX score:<http://mygraph.org/score> \
                        SELECT ?src (SUM(?score) AS ?totalScore) \
                        {?nid score: ?score . \
                        ?src link: ?dst . \
                        FILTER(?dst = ?nid) \
                        } GROUP BY ?src')

    new_scores = sparql_q.query().convert()
    s = new_scores.toxml()
    obj = xmltodict.parse(s)
    json_input = json.dumps(obj) #this is a string
    decoded = json.loads(json_input) #this is a json object(?)
    #print json.dumps(obj,sort_keys=True,indent=4)

    for i in range (len(decoded['sparql']['results']['result'])):
        nid = decoded['sparql']['results']['result'][i]['binding'][1]['uri']['#text'] 
        score = decoded['sparql']['results']['result'][i]['binding'][0]['literal']['#text']
        edge = 'http://mygraph.org/score'
        elem = '<' + nid + '> <' + edge + '> ' + score
        ins_array.append(elem)
        
    
    for item in del_array:
        sparql_u.setMethod(POST) 
        sparql_u.setQuery('DELETE DATA {'+item+'}')
        sparql_u.query()
    for item in ins_array:
        sparql_u.setMethod(POST) 
        sparql_u.setQuery('INSERT DATA {'+item+'}')
        sparql_u.query()

    sparql_q.setMethod(GET)
    sparql_q.setQuery('PREFIX score:<http://mygraph.org/score> \
                        SELECT (SUM(?score * ?score) as ?vectorSum) \
                        {?s score: ?score}')
    result = sparql_q.query().convert()
    s = result.toxml()
    obj = xmltodict.parse(s)
    json_input = json.dumps(obj) 
    decoded = json.loads(json_input) 

    sumsquare = decoded['sparql']['results']['result']['binding']['literal']['#text']
    vectorSum = math.sqrt(float(sumsquare))

    for item in ins_array:
        vectorname = item.split()[0]
        old_score = item.split()[2] 
        new_score = str(float(old_score) / float(vectorSum))
        newitem = vectorname + ' ' + item.split()[1] + ' ' + new_score
        
        sparql_u.setMethod(POST) 
        sparql_u.setQuery('DELETE DATA {'+item+'}')
        sparql_u.query()
        sparql_u.setQuery('INSERT DATA {'+newitem+'}')
        sparql_u.query()

        output_array.append(vectorname + ', ' + str(iterNo) + ', ' + new_score)

def writeToFile():
    for item in output_array:
        outputFile.write(item + '\n')

cleardata() 
populate()  
iterNo = 1
while iterNo < 50 :
    iterNo += 1
    MVM(iterNo)
    
writeToFile()

inputFile.close()
outputFile.close()


