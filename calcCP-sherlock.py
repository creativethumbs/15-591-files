#You MUST start the Sherlock database before running the programnot 

import requests

import sys
import xml.dom

import string
import math
import xmltodict, json
import string
import urllib

outputFile = open('LBNL-sherlock.txt', 'w')

output_array = [] # array for writing to output text file

userinfo = {
    'httpd_username': str(sys.argv[1]),
    'httpd_password': str(sys.argv[2])
} 

s = requests.Session()
# logs in to Sherlock
s.post('https://sherlock.psc.edu/urika/gam',data=userinfo)

headers = {'content-type': 'application/x-www-form-urlencoded'}

def CP(iterNo):  
    # check com2 pg.6
    sumofscores_a = 'PREFIX hasdest:<http://has_dest> \
                        PREFIX onport:<http://on_port> \
                        PREFIX bscore:<http://vector-b-score> \
                        PREFIX cscore:<http://vector-c-score> \
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \
                        SELECT ?srcip (SUM(xsd:double(?bscore) * xsd:double(?cscore)) AS ?totalScore) \
                        {?vector_b bscore: ?bscore . \
                        ?vector_c cscore: ?cscore . \
                        ?srcip hasdest: ?dstip . \
                        ?srcip onport: ?portnum . \
                        FILTER(?dstip = ?vector_b && ?portnum = ?vector_c) \
                        } GROUP BY ?srcip'

    sumofscores_b = 'PREFIX hasdest:<http://has_dest> \
                        PREFIX onport:<http://on_port> \
                        PREFIX ascore:<http://vector-a-score> \
                        PREFIX cscore:<http://vector-c-score> \
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \
                        SELECT ?srcip (SUM(xsd:double(?ascore) * xsd:double(?cscore)) AS ?totalScore) \
                        {?vector_a ascore: ?ascore . \
                        ?vector_c cscore: ?cscore . \
                        ?srcip hasdest: ?dstip . \
                        ?srcip onport: ?portnum . \
                        FILTER(?dstip = ?vector_a && ?portnum = ?vector_c) \
                        } GROUP BY ?srcip'

    sumofscores_c = 'PREFIX hasdest:<http://has_dest> \
                        PREFIX onport:<http://on_port> \
                        PREFIX ascore:<http://vector-a-score> \
                        PREFIX bscore:<http://vector-b-score> \
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \
                        SELECT ?srcip (SUM(xsd:double(?ascore) * xsd:double(?bscore)) AS ?totalScore) \
                        {?vector_a ascore: ?ascore . \
                        ?vector_b bscore: ?bscore . \
                        ?srcip hasdest: ?dstip . \
                        ?srcip hasdest: ?dstip2 . \
                        FILTER(?dstip = ?vector_a && ?dstip2 = ?vector_b) \
                        } GROUP BY ?srcip'

    #uses scores from previous calculation
    sumofsquares_a = 'PREFIX score:<http://vector-a-score> \
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \
                        SELECT (SUM(xsd:double(?score) * xsd:double(?score)) as ?vectorSum) \
                        {?s score: ?score}'
    sumofsquares_b = 'PREFIX score:<http://vector-b-score> \
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \
                        SELECT (SUM(xsd:double(?score) * xsd:double(?score)) as ?vectorSum) \
                        {?s score: ?score}'
    sumofsquares_c = 'PREFIX score:<http://vector-c-score> \
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \
                        SELECT (SUM(xsd:double(?score) * xsd:double(?score)) as ?vectorSum) \
                        {?s score: ?score}'

    del_array = [] # array for storing values to delete
    ins_array = [] # array for storing values to insert
    vectorSum = 0 

    # first equation ---------------------------------------------
    qsumofscores_a = {'query': sumofscores_a}
    result = s.get('https://sherlock.psc.edu/dataset/sparql/LBNL/query',params=qsumofscores_a)
     
    xml_source = result.text
    obj = xmltodict.parse(xml_source)
    json_input = json.dumps(obj)
    decoded = json.loads(json_input) 

    #print json.dumps(obj,sort_keys=True,indent=4)
    #updatea = len(decoded['sparql']['results']['result']) > 1
    # populates the array with the vector elements we need to insert
    for i in range (len(decoded['sparql']['results']['result'])):
        if (i>0):
            nid = decoded['sparql']['results']['result'][i]['binding'][0]['uri']
            score = decoded['sparql']['results']['result'][i]['binding'][1]['literal']['#text']
            edge = 'http://vector-a-score'
            elem = '<' + nid + '> <' + edge + '> "' + score + '"'
            elem2 = '<' + nid + '> <' + edge + '>'
            print elem
            ins_array.append(elem)
            del_array.append(elem2)

    print "first equation passed"

    # second equation ----------------------------------------------------
    qsumofscores_b = {'query': sumofscores_b}
    result = s.get('https://sherlock.psc.edu/dataset/sparql/LBNL/query',params=qsumofscores_b)
    
    xml_source = result.text
    obj = xmltodict.parse(xml_source)
    json_input = json.dumps(obj)
    decoded = json.loads(json_input) 

    #updateb = len(decoded['sparql']['results']['result']) > 1
    # populates the array with the vector elements we need to insert
    for i in range (len(decoded['sparql']['results']['result'])):
        if (i>0):
            nid = decoded['sparql']['results']['result'][i]['binding'][0]['uri']
            score = decoded['sparql']['results']['result'][i]['binding'][1]['literal']['#text']
            edge = 'http://vector-b-score'
            elem = '<' + nid + '> <' + edge + '> "' + score + '"'
            elem2 = '<' + nid + '> <' + edge + '>'
            print elem
            ins_array.append(elem)
            del_array.append(elem2)

    print "second equation passed"

    # third equation ----------------------------------------------------
    qsumofscores_c = {'query': sumofscores_c}
    result = s.get('https://sherlock.psc.edu/dataset/sparql/LBNL/query',params=qsumofscores_c)
    
    xml_source = result.text
    obj = xmltodict.parse(xml_source)
    json_input = json.dumps(obj)
    decoded = json.loads(json_input) 

    #print json.dumps(obj,sort_keys=True,indent=4)

    #updatec = len(decoded['sparql']['results']['result']) > 1
    # populates the array with the vector elements we need to insert
    for i in range (len(decoded['sparql']['results']['result'])):
        if (i>0):
            nid = decoded['sparql']['results']['result'][i]['binding'][0]['uri']
            score = decoded['sparql']['results']['result'][i]['binding'][1]['literal']['#text']
            edge = 'http://vector-c-score'
            elem = '<' + nid + '> <' + edge + '> "' + score + '"'
            elem2 = '<' + nid + '> <' + edge + '>'
            print elem
            ins_array.append(elem)
            del_array.append(elem2)

    print "third equation passed"

    print("ins_array has size " + str(len(ins_array)))
    # inserts all calculations into graph ---------------------------------------------------
    for i in range ( len(ins_array)):
        print str(i) 
        updatestring = 'DELETE {' + del_array[i] + ' ?o } \
                        INSERT {' + ins_array[i] +'} \
                        WHERE {' + del_array[i] + ' ?o } '
        updated = {'update': updatestring}
        s.post('https://sherlock.psc.edu/dataset/sparql/LBNL/update',headers=headers,params=updated)

    #gets the vectorSum for the first vector table -----------------------------------
    qsumofsquares_a = {'query': sumofsquares_a}
    result = s.get('https://sherlock.psc.edu/dataset/sparql/LBNL/query',params=qsumofsquares_a)

    xml_source = result.text
    obj = xmltodict.parse(xml_source)
    json_input = json.dumps(obj)
    decoded = json.loads(json_input) 

    sumsquare_a = decoded['sparql']['results']['result']['binding']['literal']['#text']   
    vectorSum_a = math.sqrt(float(sumsquare_a))

    #gets the vectorSum for the second vector table -----------------------------------
    qsumofsquares_b = {'query': sumofsquares_b}
    result = s.get('https://sherlock.psc.edu/dataset/sparql/LBNL/query',params=qsumofsquares_b)

    xml_source = result.text
    obj = xmltodict.parse(xml_source)
    json_input = json.dumps(obj)
    decoded = json.loads(json_input) 

    sumsquare_b = decoded['sparql']['results']['result']['binding']['literal']['#text']   
    vectorSum_b = math.sqrt(float(sumsquare_b))

    #gets the vectorSum for the third vector table -----------------------------------
    qsumofsquares_c = {'query': sumofsquares_c}
    result = s.get('https://sherlock.psc.edu/dataset/sparql/LBNL/query',params=qsumofsquares_c)

    xml_source = result.text
    obj = xmltodict.parse(xml_source)
    json_input = json.dumps(obj)
    decoded = json.loads(json_input) 

    sumsquare_c = decoded['sparql']['results']['result']['binding']['literal']['#text']   
    vectorSum_c = math.sqrt(float(sumsquare_c))

    #mass deletion-----------------------------------------------------------------------
    #brute force... 
    
    #print("ins_array has size " + str(len(ins_array)))----------------------------------
    print "final loop"
    idx = 0
    for item in ins_array:
        #print (item)
        sourceip = item.split()[0]
        old_score = item.split()[2][1:-1] #need to remove the double quotes
        edgelabel = item.split()[1]
        new_score = ""

        delitem = sourceip + " " + edgelabel # + " \"" + old_score + "\""
  
        if (edgelabel == '<http://vector-a-score>'):
            new_score = str(float(old_score) / float(vectorSum_a))

        elif (edgelabel == '<http://vector-b-score>'):
            new_score = str(float(old_score) / float(vectorSum_b))

        elif (edgelabel == '<http://vector-c-score>'):
            new_score = str(float(old_score) / float(vectorSum_c))

        newitem = sourceip + ' ' + edgelabel + ' "' + new_score + '"'
        print str(idx) +" "+ delitem
        print str(idx) +" "+ newitem

        #if(new_score != ""): 
        updatestring = 'DELETE {' + delitem + ' ?o } \
                    INSERT {' + newitem +'} \
                    WHERE {' + delitem + ' ?o } '
                    
        updated = {'update': updatestring}
        result = s.post('https://sherlock.psc.edu/dataset/sparql/LBNL/update',headers=headers,params=updated)
        #print result.text

        output_array.append(sourceip + ', ' + str(iterNo) + ', ' + new_score)

        idx += 1


def writeToFile():
    for item in output_array:
        outputFile.write(item + '\n')

iterNo = 1

while iterNo < 5 :
    iterNo += 1
    CP(iterNo) 
    print "done with iterNo " + str(iterNo)

writeToFile()

outputFile.close()



