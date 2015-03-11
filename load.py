#!/usr/bin/env python

import os
import json
import re
from pymongo import MongoClient
import config

def connect():
    client = MongoClient()
    db = client['disasters']
    return db
    
db = connect()    

data_dir = config.data_dir

def get_dpla(item):
    if "object" not in item:
        return None
    if item["object"] == "http://fdlp.gov/images/gpo-tn.jpg":
        return None 
    record = {
        "id": item['id'],
        "title": item["sourceResource"]["title"],
        "thumbnail": item["object"],
        "fullview": item['isShownAt'],
        "provider": item["provider"]["name"],
        "displayDate": 
            item.get("sourceResource").get("date", {}).get("displayDate"),
        "dateBegin": item.get("sourceResource").get("date", {}).get("begin"),
        "dateEnd": item.get("sourceResource").get("date", {}).get("end"),
        "description": item.get("sourceResource").get("description"),
        "rights": item.get("sourceResource").get("rights"),   
        "source": "dpla"  
    }

    if "collection" in item["sourceResource"]:
        record["coll"] = []
        try:
            record["coll"].append(item["sourceResource"]["collection"]["title"])
        except:
            for x in item["sourceResource"]["collection"]:
                record["coll"].append(x.get("title"))
         
    if "spatial" in item.get("sourceResource"):
        record["spatial"] = []
        for space in item["sourceResource"]["spatial"]:
            record["spatial"].append(space)
         
    if "subject" in item.get("sourceResource"):
       record["subjects"] = []  
       for subject in item["sourceResource"]["subject"]:
           record["subjects"].append(subject["name"])
  
    return record
    
def get_ppoc(item):
    if re.match('.*(lithograph|drawing|photomechanical|engraving|silkscreen)',
        item["medium"]) != None:
        return None
    record = {
        "id" : item["pk"],
        "title": item["title"],
        "thumbnail": item["image"]["thumb"],
        "fullview": item["links"]["resource"],
        "provider": "Library of Congress Prints and Photographs Division",
        "displayDate": item["created_published_date"],
        "coll": item["collection"],
        "subject": item["subjects"],
        "source": "ppoc"
    }
    return record

for filename in os.listdir(data_dir):
    parts = filename.split("-")
    collection = parts[0]
    source = parts[5].strip(".json")

    filename = os.path.join(data_dir, filename)

    print "loading %s" % filename

    for item in json.load(open(filename)):
        if source == "dpla":
            record = get_dpla(item)
        elif source == "ppoc":
            record = get_ppoc(item)
        else:
            raise Exception("unknown source: %s" % source)
#        print record
        if record:
            db[collection].insert(record)

