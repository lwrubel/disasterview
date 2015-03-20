from disasterview import app
from flask import render_template
from pymongo import MongoClient
import math

def connect():
    client = MongoClient()
    db = client['disasters']
    return db
    
db = connect()    

@app.route('/')
def return_cover():    
    return render_template('main.html')

@app.route('/single/')
def single_disaster():
    hurricane = db.hurricanes.find_one()
    title = hurricane['title']
    thumbnail = hurricane['thumbnail']
    return render_template('single.html', title=title, thumbnail=thumbnail)
    
@app.route('/disasters/<event_type>/', defaults={'n': 1})
@app.route('/disasters/<event_type>/<int:n>/')
def browse_images_pages(event_type, n):
    page_size = 100
    nopages = int(math.ceil( db[event_type].find().count() / page_size))   
 
    # database is not too big, so using .skip() instead of last_id-based find
    page = db[event_type].find().skip(page_size * (n - 1)).limit(page_size)
    
    return render_template('events.html', items=page, event_type=event_type, 
        nopages=nopages, pagenum=n)
    
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

#@app.route('/picker/<event_type>/')
#def image_picker(event_type):
    
