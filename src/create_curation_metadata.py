import json
from SPARQLWrapper import SPARQLWrapper
from hashlib import md5
import urllib.request

map = {}
thumbs = []

with open("/Users/nakamura/git/sim_gaikotsu/backend/data/data.json") as f:
    df = json.load(f)

new_data = {}

for index in df:
    obj = df[index]

    new_data[obj["id"]] = obj

    # break




collection_url = "https://nakamura196.github.io/gaikotsu-i/collection/collection.json"

response = urllib.request.urlopen(collection_url)
response_body = response.read().decode("utf-8")
collection = json.loads(response_body)

curations = collection["curations"]


for i in range(len(curations)):
    print(i)

    curation_url = curations[i]["@id"]


    print(curation_url)

    response = urllib.request.urlopen(curation_url)
    response_body = response.read().decode("utf-8")
    curation = json.loads(response_body)

    curation["@id"] = curation_url.replace(
        "/curation/", "/curation_m/")

    selections = curation["selections"]

    for selection in selections:

        selection["@id"] = selection["@id"].replace(
            "/curation/", "/curation_m/")

        members = selection["members"]
        if "@label" in selection["within"]:
            label = selection["within"]["@label"]
        else:
            label = selection["within"]["label"]

        for j in range(len(members)):
            member = members[j]

            id = member["@id"]

            hash = md5(id.encode('utf-8')).hexdigest()

            if hash in new_data:

                obj = new_data[hash]

                member["label"] = obj["label"]

                for m in obj["metadata"]:
                    member["metadata"].append(m)

    path = curation_url.replace("https://nakamura196.github.io/gaikotsu-i/curation/", "../docs/curation_m/")

    fw2 = open(path, 'w')
    json.dump(curation, fw2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))


'''

fw2 = open("data/base.json", 'w')
json.dump(map, fw2, ensure_ascii=False, indent=4,
          sort_keys=True, separators=(',', ': '))

print("画像総数：")
print(len(thumbs))

'''
