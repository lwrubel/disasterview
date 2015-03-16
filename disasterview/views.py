from disasterview import app
from flask import render_template
from pymongo import MongoClient

def connect():
    client = MongoClient()
    db = client['disasters']
    return db
    
db = connect()    

@app.route('/')
def single_disaster():
    hurricane = db.hurricanes.find_one()
    title = hurricane['title']
    thumbnail = hurricane['thumbnail']
    return render_template('index.html', title=title, thumbnail=thumbnail)
    
@app.route('/disasters/<event_type>/')
def browse_images(event_type):
    items = list(db[event_type].find())
    thumbnails = []
    # temporarily limiting number of items displayed
    for i in range(0,24):
        thumbnails.append(items[i])
    return render_template('events.html', items=thumbnails, event_type=event_type)  
