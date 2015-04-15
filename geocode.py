#!/usr/bin/env python

from pymongo import MongoClient
import requests
import json	
from bson.json_util import dumps
from time import sleep

def connect():
    client = MongoClient()
    db = client['disasters']
    return db
    
db = connect()

# names of collections in database
disasters = ['hurricanes','floods','earthquakes','forest',]

# first, get coordinates for PPOC items from LOC new search API
loc_url = 'http://loc.gov/item/'
query = {'fo':'json', 'at':'item'}

def loc_lookup():
    print 'looking up at loc.gov'
    session = requests.Session()
    for disaster in disasters:
        items = db[disaster].find({'source': 'ppoc'})
        for item in items:
            url = loc_url + item['id']
            sleep(.5)
            try:
                print 'checking ', url 
                response = session.get(url, params=query).json()
                coordinates = response['item'].get('latlong')
                if coordinates == None:
                    pass
                else:
                    points = []
                    points.append(coordinates)
                    print "found coordinates"
                    db[disaster].update({'id': item['id']},{'$set':{'points': points}})                    
            except ValueError:
                print 'ValueError', url
            except AttributeError: # ids formatted with slashes?
                print 'AttributeError', url
            
# next, test *all* ppoc coordinates for being in US bounding box, roughly:
# (NE 49.590370, -66.932640, SW 24.949320, -125.001106)

def check_coordinates():
    print 'checking coordinates'
    for disaster in disasters:
        items = db[disaster].find({'source': 'ppoc', 'points': {'$exists' : True}})
        for item in items:
            latlong = item['points'][0].split(',')
            if (24.949320 <= float(latlong[0]) <= 49.590370) and (-125.001106 <= float(latlong[1]) <= -66.932640):
		        pass
            else:
                with open('flagged_records.json','a') as fp:
                    fp.write(dumps(item))
                db[disaster].update({'id': item['id']},{'$unset':{'points': ''}})


# check DPLA country field (enhanced geodata) for non-US
def check_country():
    print 'checking dpla country data'
    for disaster in disasters:
        items = db[disaster].find({'source': 'dpla', 'spatial': {'$exists' : True}})
        for item in items:
            for space in item['spatial']:
                if space.get('country'):
                    if space.get('country') != "United States":
                        #remove the geo coordinates from that record since it's questionable
                        db[disaster].update({'id': item['id']},{'$unset':{'points': ''}})
           
if __name__ == '__main__':
   loc_lookup()
   check_coordinates()
   check_country()	



