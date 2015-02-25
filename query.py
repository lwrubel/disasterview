import requests
import json
from datetime import datetime
from config import dpla_api_key, data_dir

today = datetime.now()

# create request for each disaster, using pagination
def getdata(disasters):
    for subject in disasters:    
        p = 1  # start with first page 
        size = 500 # results size
        
        data = requestdata(subject, p, size) # first call to get count
        createfile(data, subject, p) # write first call 
        
        json = data.json() # get the json from the response object
        pages = json['count'] / size  # get number of pages 
        
        for i in range(pages): # iterate through pages
            p = i + 2  # to skip over page "0" (doesn't exist) 
                          # and "1" (already got it)
            data = requestdata(subject, p, size)
            createfile(data, subject, p) 
     
# make request to dpla        
def requestdata(subject, p, size):
    query = {'api_key':dpla_api_key, 'sourceResource.subject.name':subject, 
            'sourceResource.type':'image', 'page_size':size, 'page':p, 
            'fields':'id,isShownAt,object,provider,sourceResource'}
    r = requests.get('http://api.dp.la/v2/items?', params=query)
    return r

# create time-stamped and page-stamped files
def createfile(data, subject, p):
    records = processdata(data) 
    filename = data_dir + '{0}-{1}-{2}.json'.format(subject,today.isoformat(), p)
    f = open(filename, 'w')
    f.write(records) 
    f.close()


# pull out records from docs 
def processdata(data): 
    response = data.json()
    items = json.dumps(response['docs']) # creates a string (json) which can be
                                         # written to file    
    return items 
    
disasters = ['earthquakes','hurricanes','floods','forests+AND+fires']

getdata(disasters)



