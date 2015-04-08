from disasterview import app
from flask import render_template, request
from pymongo import MongoClient
import math

def connect():
    client = MongoClient()
    db = client['disasters']
    return db
    
db = connect()    

names = {'earthquakes':'earthquakes','floods': 'floods','forest': 'forest fires','hurricanes':'hurricanes'}

@app.route('/')
def return_cover():    
    return render_template('main.html')


@app.route('/credits/')
def show_credits():
    return render_template('about.html')


@app.route('/disasters/<event_type>/', defaults={'n': 1})
@app.route('/disasters/<event_type>/<int:n>/')
def browse_images_pages(event_type, n):
    page_size = 100 
    nopages = int(math.ceil( float(db[event_type].find().count()) / float(page_size)))   
 
    # database is not too big, so using .skip() instead of last_id-based find
    if nopages > 1:
        page = db[event_type].find().skip(page_size * (n - 1)).limit(page_size)
    else:
        page = db[event_type].find()
        
    return render_template('events.html', items=page, event_type=event_type, 
        nopages=nopages, pagenum=n, label=names[event_type])
  
    
@app.route('/map/')
def show_map(): 
    items = []
    # names of collections in database
    disasters = ['earthquakes','floods','forest','hurricanes']
    for disaster in disasters:
        # get all records that have coordinates in points list
        locations = list(db[disaster].find({"points" : { "$exists" : True}}))    
        for location in locations:
            for point in location['points']:
                items.append({'point': point,'title': location['title'], 
                    'url': location['nativeView'], 'thumbnail': location['thumbnail'], 'disaster': disaster})
    return render_template('map.html', items=items)


@app.route('/items/')
def picklist():
    items = []
    for key in request.args.keys():
        if key != "count":
            parts = key.split('_')
            event_type = parts[1]
            record_id = request.args.get(key)
            item = db[event_type].find_one({'id' : record_id})
            items.append(item)
    return render_template('items.html', items=items)
    
    