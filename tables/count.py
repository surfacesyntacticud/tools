import glob
import json
import os

collections = ["meta", "ud_deps", "sud_deps", "ud_feats", "SP_ud_meta", "SP_ud_deps", "SP_ud_feats"]

dict={}

def scan (coll):
  subfiles = glob.glob("%s/*.json" % coll)
  dict[coll] = len(subfiles)
  for subfile in subfiles:
    with open(subfile) as jsonFile:
      jsonObject = json.load(jsonFile)
      jsonFile.close()
    wihtout_ext = os.path.splitext(subfile)[0]
    dict[wihtout_ext] = len(jsonObject["columns"])

for coll in collections:
  scan (coll)

with open("count.json", "w") as file:
  json.dump(dict, file, indent=2)
