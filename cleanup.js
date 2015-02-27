// removes sets of documents not relevant to the app

conn = new Mongo();
db = conn.getDB("disasters");

// images of agency activities, mostly not of disasters themselves
db.hurricanes.remove({
    "sourceResource.collection.id" : "dfd693cc7db3865a78d62523b3d3f124" 
    });

// no thumbnail provided
db.floods.remove({
    "object" : null 
    });

// thumbnail is of GPO logo; no image available
db.floods.remove({ 
    "object" : "http://fdlp.gov/images/gpo-tn.jpg"
    });
db.earthquakes.remove({ 
    "object" : "http://fdlp.gov/images/gpo-tn.jpg"
    });
db.hurricanes.remove({ 
    "object" : "http://fdlp.gov/images/gpo-tn.jpg"
    });


