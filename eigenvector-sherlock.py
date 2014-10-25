#You MUST start the Sherlock database before running the program!

import requests

import sys
import xml.dom

import string
import math
import xmltodict, json
import string
import urllib

outputFile = open('eigenvector-sherlock.txt', 'w')

output_array = [] # array for writing to output text file

userinfo = {
    'httpd_username': 'YOUR USERNAME',
    'httpd_password': 'YOUR PASSWORD'
}

# some predefined queries / updates used
allscores = 'PREFIX score:<http://mygraph.org/score> \
SELECT ?s ?p ?o \
{?s ?p ?o . \
FILTER(?p = score:)} '

sumofscores = 'PREFIX link:<http://mygraph.org/linkedto> \
                        PREFIX score:<http://mygraph.org/score> \
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \
                        SELECT ?src (SUM(xsd:double(?score)) AS ?totalScore) \
                        {?nid score: ?score . \
                        ?src link: ?dst . \
                        FILTER(?dst = ?nid) \
                        } GROUP BY ?src'

sumofsquares = 'PREFIX score:<http://mygraph.org/score> \
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \
                        SELECT (SUM(xsd:double(?score) * xsd:double(?score)) as ?vectorSum) \
                        {?s score: ?score}'
def MVM(iterNo): 
    del_array = [] # array for storing values to delete
    ins_array = [] # array for storing values to insert
    vectorSum = 0

    query1 = {'query': allscores}
    result = requests.post('https://sherlock.psc.edu/dataset/sparql/eigenvector/query',data=userinfo,params=query1)

    xml_source = result.text
    obj = xmltodict.parse(xml_source)
    json_input = json.dumps(obj)
    decoded = json.loads(json_input) 

    #print json.dumps(obj,sort_keys=True,indent=4)

    # populates the array with the vector elements we need to delete later
    for i in range (len(decoded['sparql']['results']['result'])):
        nid = decoded['sparql']['results']['result'][i]['binding'][0]['uri']
        edge = decoded['sparql']['results']['result'][i]['binding'][1]['uri']
        score = decoded['sparql']['results']['result'][i]['binding'][2]['literal']
        elem = '<' + nid + '> <' + edge + '> "' + score + '"'
        del_array.append(elem) 

        if (iterNo == 2):
            output_array.append('<'+nid+'>, 1, 0.001')

    query2 = {'query': sumofscores}
    result = requests.post('https://sherlock.psc.edu/dataset/sparql/eigenvector/query',data=userinfo,params=query2)

    xml_source = result.text
    obj = xmltodict.parse(xml_source)
    json_input = json.dumps(obj)
    decoded = json.loads(json_input) 

    #print json.dumps(obj,sort_keys=True,indent=4)

    # populates the array with the vector elements we need to insert
    for i in range (len(decoded['sparql']['results']['result'])):
        nid = decoded['sparql']['results']['result'][i]['binding'][0]['uri']
        score = decoded['sparql']['results']['result'][i]['binding'][1]['literal']['#text']
        edge = 'http://mygraph.org/score'
        elem = '<' + nid + '> <' + edge + '> "' + score + '"'
        ins_array.append(elem)

    #does the SQL update using elements we need to insert and delete
    for item in del_array:
        updatestring ={'update': 'DELETE DATA {'+item+'}'}
        requests.post('https://sherlock.psc.edu/dataset/sparql/eigenvector/update',data=userinfo,params=updatestring)

    for item in ins_array:
        updatestring ={'update': 'INSERT DATA {'+item+'}'}
        requests.post('https://sherlock.psc.edu/dataset/sparql/eigenvector/update',data=userinfo,params=updatestring)


    query3 = {'query': sumofsquares}
    result = requests.post('https://sherlock.psc.edu/dataset/sparql/eigenvector/query',data=userinfo,params=query3)

    xml_source = result.text
    obj = xmltodict.parse(xml_source)
    json_input = json.dumps(obj)
    decoded = json.loads(json_input) 

    sumsquare = decoded['sparql']['results']['result']['binding']['literal']['#text']
    print "sumsquare is " + sumsquare
    vectorSum = math.sqrt(float(sumsquare))

    for item in ins_array:
        vectorname = item.split()[0]
        old_score = item.split()[2][1:-1] #need to remove the double quotes
        new_score = str(float(old_score) / float(vectorSum))
        newitem = vectorname + ' ' + item.split()[1] + ' "' + new_score + '"'
        
        deletestring ={'update': 'DELETE DATA {'+item+'}'}
        insertstring ={'update': 'INSERT DATA {'+newitem+'}'}

        requests.post('https://sherlock.psc.edu/dataset/sparql/eigenvector/update',data=userinfo,params=deletestring)
        requests.post('https://sherlock.psc.edu/dataset/sparql/eigenvector/update',data=userinfo,params=insertstring)

        output_array.append(vectorname + ', ' + str(iterNo) + ', ' + new_score)


def writeToFile():
    for item in output_array:
        outputFile.write(item + '\n')

iterNo = 1
while iterNo < 50 :
    iterNo += 1
    MVM(iterNo) 
    print "done with iterNo " + str(iterNo)

writeToFile()

outputFile.close()



