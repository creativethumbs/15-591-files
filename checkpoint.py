# Creates a Sherlock checkpoint
# Make sure to start your database before running the code!
 
import requests

import sys
import xml.dom

import string
import math
import xmltodict, json
import string
import urllib

from time import gmtime, strftime

def makeCheckpoint():
    if (len(sys.argv)==1):
        print "To compile the code, run checkpoint.py [Sherlock username] [password]"
    else:
        userinfo = {
            'httpd_username': str(sys.argv[1]),
            'httpd_password': str(sys.argv[2])
        } 
        with requests.Session() as s: 
            req = s.post('https://sherlock.psc.edu/urika/gam',data=userinfo)
            
            req = s.get('https://sherlock.psc.edu/urika-admin/public/api/db/running')
            
            decoded = json.loads(req.text) 
            databaseid = decoded['id']
            
            name = {'name': strftime("%Y-%m-%d %H:%M:%S", gmtime())}
            wait = {'wait': 'false'}
            req = s.post('https://sherlock.psc.edu/urika-admin/public/api/db/'+databaseid+'/checkpoint',data=name,params=wait)
            
            print 'Checkpoint created! Name: ' + name['name']

makeCheckpoint()



