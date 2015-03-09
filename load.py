#!/usr/bin/env python

import os
import json
import pymongo

db = pymongo.connect("disasters")
data_dir = "data/files"

def get_dpla(item):
    record = {
        "title": item["sourceResource"]["title"],
        "thumbnail": item["object"]
    }
    return record

def get_ppoc(item):
    record = {
        "title": item["title"],
        "thumbnail": item["image.thumb"]
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
        print record
        #db.insert(record)

