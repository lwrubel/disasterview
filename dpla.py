import requests
import json
import re
from datetime import datetime
from config import dpla_api_key, data_dir

today = datetime.now()

# create request for each disaster, using pagination
def getdata(disasters):
    for subject in disasters:    
        p = 1  # start with first page 
        size = 500 # results size
        
        data = requestdata(subject, p, size) # first call to get count
        createfile(data['docs'], subject, p) # write first call 
        
        pages = data['count'] / size  # get number of pages 
        
        for i in range(pages): # iterate through pages
            p = i + 2  # skips over page "0" (doesn't exist) 
                       # and "1" (already got it); get modulo
            data = requestdata(subject, p, size)
            createfile(data['docs'], subject, p) 
     
# make request to dpla        
def requestdata(subject, p, size):
    query = {'api_key':dpla_api_key, 'sourceResource.subject.name':subject, 
            'sourceResource.type':'image', 'page_size':size, 'page':p, 
            'fields':'id,isShownAt,object,provider,sourceResource'}
    r = requests.get('http://api.dp.la/v2/items?', params=query)
    return r.json()

# create time-stamped and page-stamped files
def createfile(data, subject, p):
    e = re.compile('\W.*') # regex to simplify search statements that have 
                           # punctuation or boolean
    subject = e.sub('', subject)
    filename = data_dir + '{0}-{1}-{2}-dpla.json'.format(subject,today.isoformat(), p)
    f = open(filename, 'w')
    f.write(json.dumps(data)) 
    f.close()
    
disasters = ['earthquakes','hurricanes','floods','forest+AND+fires']

getdata(disasters)



