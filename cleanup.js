// removes documents not relevant to the app

db = new Mongo().getDB("disasters")

var deletes = [ 
    {msg: "non-disaster images of agencies", coll: "hurricanes", fields: { "sourceResource.collection.id" : "dfd693cc7db3865a78d62523b3d3f124" }}, 
    {msg: "no thumbnail", coll: "floods", fields: { object: null }}, 
    {msg: "image is GPO logo", coll: "floods", fields: { object: "http://fdlp.gov/images/gpo-tn.jpg" }}, 
    {msg: "image is GPO logo", coll: "earthquakes", fields: { object: "http://fdlp.gov/images/gpo-tn.jpg" }}, 
    {msg: "image is GPO logo", coll: "hurricanes", fields: { object: "http://fdlp.gov/images/gpo-tn"}},
    {msg: "non-photo image", coll: "forest", fields: { medium: { $regex: /lithograph|drawing|photomechanical/ }}},
    {msg: "non-photo image", coll: "hurricanes", fields: { medium: { $regex: /lithograph|drawing|photomechanical/ }}},
    {msg: "non-photo image", coll: "floods", fields: { medium: { $regex: /lithograph|drawing|photomechanical/ }}},
    {msg: "non-photo image", coll: "earthquakes", fields: { medium: { $regex: /lithograph|drawing|photomechanical/ }}}
    ]
    
for (var i = 0; i < deletes.length; i++) {
    var col = deletes[i].coll
    print("deleting docs from " + col + ": " + deletes[i].msg)
    db[col].remove( deletes[i].fields )
    }

