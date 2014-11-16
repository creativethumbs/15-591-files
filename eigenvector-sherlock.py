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
    'httpd_username': str(sys.argv[1]),
    'httpd_password': str(sys.argv[2])
} 

s = requests.Session()
# logs in to Sherlock
s.post('https://sherlock.psc.edu/urika/gam',data=userinfo)

headers = {'content-type': 'application/x-www-form-urlencoded'}

def MVM(iterNo): 
    #all scores from previous iteration
    allscores = 'PREFIX score:<http://scoreiter'+str(iterNo-1)+'> \
    SELECT ?s ?p ?o \
    {?s ?p ?o . \
    FILTER(?p = score:)} '

    sumofscores = 'PREFIX link:<http://link> \
                        PREFIX score:<http://scoreiter'+str(iterNo-1)+'> \
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \
                        SELECT ?src (SUM(xsd:double(?score)) AS ?totalScore) \
                        {?nid score: ?score . \
                        ?src link: ?dst . \
                        FILTER(?dst = ?nid) \
                        } GROUP BY ?src'

    #mass deletion
    deletescores = 'PREFIX score:<http://scoreiter'+str(iterNo)+'> \
                    DELETE {?s ?p ?o} WHERE {?s ?p ?o . \
                    FILTER (?p = score:)}'

    #uses scores from previous calculation
    sumofsquares = 'PREFIX score:<http://scoreiter'+str(iterNo)+'> \
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \
                        SELECT (SUM(xsd:double(?score) * xsd:double(?score)) as ?vectorSum) \
                        {?s score: ?score}'

    del_array = [] # array for storing values to delete
    ins_array = [] # array for storing values to insert
    vectorSum = 0 

    query2 = {'query': sumofscores}
    result = s.get('https://sherlock.psc.edu/dataset/sparql/eigenvector2/query',params=query2)
    
    xml_source = result.text
    obj = xmltodict.parse(xml_source)
    json_input = json.dumps(obj)
    decoded = json.loads(json_input) 

    # populates the array with the vector elements we need to insert
    for i in range (len(decoded['sparql']['results']['result'])):
        nid = decoded['sparql']['results']['result'][i]['binding'][0]['uri']
        score = decoded['sparql']['results']['result'][i]['binding'][1]['literal']['#text']
        edge = 'http://scoreiter'+str(iterNo)
        elem = '<' + nid + '> <' + edge + '> "' + score + '"'
        
        ins_array.append(elem)

    updatestring = ''
    for item in ins_array:
        updatestring += 'INSERT DATA {'+item+'}; ' 
    
    print str(len(updatestring))
    updated ={'update': updatestring}
    status = s.post('https://sherlock.psc.edu/dataset/sparql/eigenvector2/update',headers=headers,params=updated)
    print status.text
    
    query3 = {'query': sumofsquares}
    result = s.get('https://sherlock.psc.edu/dataset/sparql/eigenvector2/query',params=query3)

    xml_source = result.text
    obj = xmltodict.parse(xml_source)
    json_input = json.dumps(obj)
    decoded = json.loads(json_input) 

    sumsquare = decoded['sparql']['results']['result']['binding']['literal']['#text']
    
    vectorSum = math.sqrt(float(sumsquare))

    #deletes all scores from the previous calculation so they can be updated
    deletestring ={'update': deletescores}
    s.post('https://sherlock.psc.edu/dataset/sparql/eigenvector2/update',headers=headers,params=deletestring)

    insertstring = ''
    for item in ins_array:
        vectorname = item.split()[0]
        old_score = item.split()[2][1:-1] #need to remove the double quotes
        new_score = str(float(old_score) / float(vectorSum))
        newitem = vectorname + ' ' + item.split()[1] + ' "' + new_score + '"'
        
        insertstring += 'INSERT DATA {'+newitem+'}; '

        output_array.append(vectorname + ', ' + str(iterNo) + ', ' + new_score)

    updated = {'update': insertstring}
    status2 = s.post('https://sherlock.psc.edu/dataset/sparql/eigenvector2/update',headers=headers,params=updated)
    print status2.text


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



