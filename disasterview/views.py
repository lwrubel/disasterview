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
    title = hurricane['sourceResource']['title']
    thumb = hurricane['object']
    return render_template('index.html', title=title, thumb=thumb)
    
@app.route('/hurricanes/')
def browse_images():
    items = list(db.hurricanes.find({}))
    
    return render_template('hurricanes.html', items=items) 


