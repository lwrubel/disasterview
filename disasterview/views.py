from disasterview import app
from flask import render_template
from pymongo import MongoClient

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
    
@app.route('/disasters/<event_type>/')
def browse_images(event_type): # event_type is a database collection
    items = list(db[event_type].find())
    thumbnails = []
    # temporarily limiting number of items displayed
    for i in range(0,24):
        thumbnails.append(items[i])
    return render_template('events.html', items=thumbnails, event_type=event_type)  

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
                    'url': location['platformView'], 'disaster': disaster})
    return render_template('map.html', items=items)

#experimenting with paging to support infinite scroll, not finished
@app.route('/pages/')
def page_results():
    event_type = 'floods'
    all = db[event_type].find().count()
    # page 1

    n = 24
    while n < (all / n):
        items = list(db[event_type].find().limit(n))
        last_id = items[(n-1)]['_id']
        x = list(db[event_type].find({'_id'> last_id}).limit(n))
    return render_template('pages.html', items=items, event_type=event_type,
        last_id=last_id)

