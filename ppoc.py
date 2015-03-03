import requests
import json
import re
from urlparse import *
from datetime import datetime
from config import data_dir

today = datetime.now()
              
url = 'http://loc.gov/pictures/search/?'
query = {'c':50, 'sp': 1, 'fo':'json', 'co!':'hh', #exclude HAER, HABS  
         'fa': 'displayed:anywhere', 'fi': 'subject' }

def getdata(disasters):
    for subject in disasters:
        query['q'] = subject
        r = requests.get(url, params=query)
        print r.url
        response = r.json()
        createfile(response['results'], subject, query['sp'])
        
        while response['pages']['next']: # get rest of pages
            link = response['pages']['next'] + '&fo=json'
            r = requests.get(link)
            response = r.json()
            params = parse_qs(urlparse(r.url).query) # creates dict out of params in url
            createfile(response['results'], subject, params['sp'][0])
 
# write response to timestamped and pagestamped files          
def createfile(data, subject, page):
    e = re.compile('\W.*') 
    subject = e.sub('', subject)
    filename = data_dir + '{0}-{1}-{2}-ppoc.json'.format(subject,today.isoformat(),page)
    f = open(filename, 'w')
    f.write(json.dumps(data)) 
    f.close()

disasters = ['earthquakes','hurricanes','floods','forest fires']

getdata(disasters)
        