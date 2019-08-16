import glob
import numpy
import json
import urllib.request
import csv
from hashlib import md5
import os
import requests
import shutil


odir = "data/images"

collection_url = "https://archdataset.dl.itc.u-tokyo.ac.jp/collections/gaikotsu/image/collection.json"

response = urllib.request.urlopen(collection_url)
response_body = response.read().decode("utf-8")
collection = json.loads(response_body)

manifests = collection["manifests"]

hs = 600

for m in manifests:

    manifest_uri = m["@id"]
    print(manifest_uri)

    response = urllib.request.urlopen(manifest_uri)
    response_body = response.read().decode("utf-8")
    manifest = json.loads(response_body)

    canvases = manifest["sequences"][0]["canvases"]

    count = 1

    members = []

    for canvas in canvases:
        canvas_uri = canvas["@id"]
        image_api = canvas["thumbnail"]["service"]["@id"]
        url = image_api+"/full/,"+str(hs)+"/0/default.jpg"
        hash = md5(url.encode('utf-8')).hexdigest()

        file = "/Users/nakamura/git/keras-yolo32/gaikotsu/data/json/"+hash+".jpg.json"

        if os.path.exists(file):

            try:

                with open(file) as f:
                    df = json.load(f)

                height = canvas["height"]
                r = height / hs

                for obj in df:
                    x = int(obj["left"] * r)
                    y = int(obj["top"] * r)
                    w = int(obj["right"] * r - x)
                    h = int(obj["buttom"] * r - y)
                    xywh = str(x)+","+str(y)+","+str(w)+","+str(h)

                    member = {
                        "@id": canvas_uri+"#xywh="+xywh,
                        "@type": "sc:Canvas",
                        "label": "["+str(count)+"]",
                        "metadata": [
                            {
                                "label": "Score",
                                "value": obj["score"]
                            }
                        ],
                        "thumbnail": image_api+"/"+xywh+"/,300/0/default.jpg"
                    }

                    count += 1

                    members.append(member)

            except:
                print("*** Error: "+file)

    if len(members) > 0:

        hash = md5(manifest_uri.encode('utf-8')).hexdigest()

        curation = {
            "@context": [
                "http://iiif.io/api/presentation/2/context.json",
                "http://codh.rois.ac.jp/iiif/curation/1/context.json"
            ],
            "@id": "https://nakamura196.github.io/gaikotsu-i/curation/"+hash+".json",
            "@type": "cr:Curation",
            "label": "Curating list",
            "selections": [
                {
                    "@id": "https://nakamura196.github.io/gaikotsu-i/curation/"+hash+".json/range1",
                    "@type": "sc:Range",
                    "label": "Manual curation by IIIF Curation Viewer",
                    "members": members,
                    "within": {
                        "@id": manifest_uri,
                        "@type": "sc:Manifest",
                        "label": manifest["label"]
                    }
                }
            ]
        }

        fw = open("../docs/curation/"+hash+".json", 'w')
        json.dump(curation, fw, ensure_ascii=False, indent=4,
                  sort_keys=True, separators=(',', ': '))
