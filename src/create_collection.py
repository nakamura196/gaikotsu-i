import glob
import json


files = glob.glob("../docs/curation/*.json")

collection = {
    "@context": "http://iiif.io/api/presentation/2/context.json",
    "@id": "https://nakamura196.github.io/gaikotsu-i/collection/collection.json",
    "@type": "cr:Collection",
    "label": "宮武外骨蒐集資料",
    "curations": []
}

for file in files:
    with open(file) as f:
        df = json.load(f)

    print(file)

    if "@label" in df["selections"][0]["within"]:
        label = df["selections"][0]["within"]["@label"]
    else:
        label = df["selections"][0]["within"]["label"]

    curation_obj = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": df["@id"],
        "@type": "cr:Curation",
        "label": label
    }
    collection["curations"].append(curation_obj)


with open("../docs/collection/collection.json", 'w') as f:
    json.dump(collection, f, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))





