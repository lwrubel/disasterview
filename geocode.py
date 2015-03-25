from pymongo import MongoClient
import requests
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

# where no coordinates remaining, try to look up using GeoNames API
    
#    for subject in subjects['subject']:
#        subject.split('--')
#        if subject[0] == 'United States':
#            places.append({'state': subject[1], 'sublocation': subject[2]})




