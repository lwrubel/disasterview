from pymongo import MongoClient
import requests
import json
from config import geonames_user	

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
    for disaster in disasters:
        items = db[disaster].find({'source': 'ppoc'})
        for item in items:
            url = loc_url + item['id']
            try:
                response = requests.get(url, params=query).json()
                coordinates = response['item'].get('latlong')
                if coordinates == None:
                    pass
                else:
                    points = []
                    points.append(coordinates)
                    db[disaster].update({'id': item['id']},{'$set':{'points': points}})
            except ValueError:
                print 'ValueError', url
            except AttributeError:
                print 'AttributeError', url
            
# next, test all coordinates for being in US bounding box
# rough coordinates for continental US bounding box
# NE 49.590370, -66.932640, SW 24.949320, -125.001106

def check_coordinates():
    print 'checking coordinates'
    for disaster in disasters:
        items = db[disaster].find({'source': 'ppoc', 'points': {'$exists' : True}})
        for item in items:
		    latlong = item['points'][0].split(',')
		    if (24.949320 <= float(latlong[0]) <= 49.590370) and (-125.001106 <= float(latlong[1]) <= -66.932640):
			    pass
		    else:
			    f = open('flagged_records','a')
			    f.write(str(item))
			    f.close()
			    # delete points field from record in database
			    db[disaster].update({'id': item['id']},{'$unset':{'points': ''}})

# where no coordinates remaining, try to look up using GeoNames API
    
#    for subject in subjects['subject']:
#        subject.split('--')
#        if subject[0] == 'United States':
#            places.append({'state': subject[1], 'sublocation': subject[2]})

if __name__ == '__main__':
    loc_lookup()
    check_coordinates()
	



