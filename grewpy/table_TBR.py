import argparse
import json
import datetime
from grewpy import Request, Corpus, set_config

parser = argparse.ArgumentParser(description="Build a Grew-table from a list of treebanks and a list of requests")
parser.add_argument("treebanks", help="a JSON file with the list of treebanks")
parser.add_argument("requests", help="a JSON file with the list of requests")
parser.add_argument("-i", "--instance", help="grew-match instance", default="https://universal.grew.fr")
parser.add_argument("-t", "--title", help="title of the table")
parser.add_argument("-c", "--config", help="grew config")
args = parser.parse_args()

with open(args.requests, "rb") as f:
  data = json.load(f)
  grew_requests = { id: Request.from_json(data[id]["request"]) for id in data }
  def text_request(id):
    text = str(grew_requests[id])
    if "comment" in data[id]:
      return f'{data[id]["comment"].replace("%", "%25")}\n{text}'.replace("\n", "%0A")
    else:
      return f'{text}'.replace("\n", "%0A")
  text_requests = { id: text_request(id) for id in data }

with open(args.treebanks, "rb") as f:
  corpora = json.load(f)

if args.title:
  title = args.title
else:
  title = "## Table Treebanks/request"

if args.config:
  set_config(args.config)

if __name__ == '__main__':
  main_dict = {}
  for corpus_id in corpora:
    corpus = Corpus(corpora[corpus_id])
    main_dict[corpus_id] = { id: corpus.count(grew_requests[id]) for id in grew_requests }
    corpus.clean()

  columns = [ {"field": id, "headerName": id} for id in grew_requests]
  columns_total = {"row_header": "Treebank", "row_type": "TOTAL"} | { id: sum([main_dict[corpus_id][id] for corpus_id in corpora]) for id in grew_requests }

  cells = [ {"row_header": k1, "row_total": sum(main_dict[k1].values())} | { k2: [main_dict[k1][k2]] for k2 in main_dict[k1]} for k1 in main_dict]

  data = {
    "kind": "TBR",
    "title": title,
    "timestamp": datetime.datetime.now().isoformat(),
    "col_key": "Request",
    "columns": columns, 
    "columns_total": columns_total, 
    "requests": text_requests,
    "cells": cells,
    "display_modes": [["occ", "NUM"]],
    "grew_match_instance": args.instance,
    "grew_match": {}
  }

  print (json.dumps(data, indent=2))
