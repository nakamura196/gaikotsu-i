import glob
import numpy
import json
import urllib.request
import csv
from hashlib import md5
import os
import requests
import shutil


def download_img(url, file_name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    else:
        print("error")

odir = "data/images"

collection_url = "https://archdataset.dl.itc.u-tokyo.ac.jp/collections/gaikotsu/image/collection.json"

response = urllib.request.urlopen(collection_url)
response_body = response.read().decode("utf-8")
collection = json.loads(response_body)

manifests = collection["manifests"]

for m in manifests:

    manifest_uri = m["@id"]
    print(manifest_uri)

    response = urllib.request.urlopen(manifest_uri)
    response_body = response.read().decode("utf-8")
    manifest = json.loads(response_body)

    canvases = manifest["sequences"][0]["canvases"]

    for canvas in canvases:
        url = canvas["thumbnail"]["service"]["@id"]+"/full/,600/0/default.jpg"
        hash = md5(url.encode('utf-8')).hexdigest()
        download_img(url, odir+"/"+hash+".jpg")
