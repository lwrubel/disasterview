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
    
@app.route('/disasters/hurricanes/')
def browse_hurricane_images():
    items = list(db.hurricanes.find())
    return render_template('hurricanes.html', items=items) 
	#needs thumbnail, maybe later include more 

@app.route('/disasters/floods/')
def floods_view():    
    items = list(db.floods.find({}))
    return render_template('hurricanes.html', items=items)


@app.route('/disasters/forestfires/')
def forestfires_view():    
    items = list(db.forest.find({}))
    return render_template('hurricanes.html', items=items)

