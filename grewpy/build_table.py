import sys
import argparse
import json
import datetime
from grewpy import Request, Corpus, set_config

parser = argparse.ArgumentParser(description="Build a Grew table from a list of treebanks and a list of requests")
parser.add_argument("kind", help="the kind of table to build: TBR (treebanks/requests) or TBC (treebanks/clustering)")
parser.add_argument("--treebanks", help="a JSON file with the list of treebanks")
parser.add_argument("--requests", help="[TBR only ] a JSON file with the list of requests")
parser.add_argument("--request", help="[TBC only ] a JSON file with the main request")
parser.add_argument("--clustering_key", help="[TBC only ] the key used for clustering")
parser.add_argument("-i", "--instance", help="grew-match instance", default="https://universal.grew.fr")
parser.add_argument("-t", "--title", help="title of the table")
parser.add_argument("-c", "--config", help="grew config")
args = parser.parse_args()

if args.config:
  set_config(args.config)

if args.title:
  title = args.title
elif args.kind == "TBR":
  title = "## Table treebanks/request"
elif args.kind == "TBC":
  title = "## Table treebanks/clustering"
else:
  print (f"Unknown kind {args.kind}", file=sys.stderr)
  raise ValueError

if args.treebanks:
  with open(args.treebanks, "rb") as f:
    corpora = json.load(f)
else:
  print (f"Missing --treebanks", file=sys.stderr)
  raise ValueError



if __name__ == '__main__' and args.kind == "TBR":
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

  main_dict = {}
  for corpus_id in corpora:
    corpus = Corpus(corpora[corpus_id])
    main_dict[corpus_id] = { id: corpus.count(grew_requests[id]) for id in grew_requests }
    corpus.clean()

  columns = [ {"field": id, "headerName": id} for id in grew_requests]
  columns_total = {"row_header": "Treebank", "row_type": "TOTAL"} | { id: sum([main_dict[corpus_id][id] for corpus_id in corpora]) for id in grew_requests }

  cells = [ {"row_header": k1, "row_total": sum(main_dict[k1].values())} | { k2: [main_dict[k1][k2]] for k2 in main_dict[k1]} for k1 in main_dict]

  output = {
    "kind": "TBR",
    "title": title,
    "timestamp": datetime.datetime.now().isoformat(),
    "grew_match_instance": args.instance,
    "requests": text_requests,
    "col_key": "Request",
    "columns": columns, 
    "columns_total": columns_total, 
    "cells": cells,
    "display_modes": [["occ", "NUM"]],
  }

  print (json.dumps(output, indent=2))




if __name__ == '__main__' and args.kind == "TBC":

  if args.request:
    with open(args.request, "rb") as f:
      data = json.load(f)
      grew_request = Request.from_json(data["request"])
      text = str(grew_request)
      if "comment" in data:
        text_request = f'{data["comment"].replace("%", "%25")}\n{text}'.replace("\n", "%0A")
      else:
        text_request = f'{text}'.replace("\n", "%0A")
  else:
    print (f"Missing --request", file=sys.stderr)
    raise ValueError

  if args.clustering_key:
    clustering_key = args.clustering_key
  else:
    print (f"Missing --clustering_key", file=sys.stderr)
    raise ValueError

  main_dict = {}
  for corpus_id in corpora:
    corpus = Corpus(corpora[corpus_id])
    main_dict[corpus_id] = corpus.count(grew_request, clustering_keys=[clustering_key])
    corpus.clean()

  def esc(s):
    return s.replace(".", "_")

  columns_dict = dict()
  for corpus_id in main_dict:
    for k2 in main_dict[corpus_id]:
      columns_dict[k2] = main_dict[corpus_id][k2] + columns_dict.get(k2, 0)
  column_list = [(c, columns_dict[c]) for c in columns_dict]
  column_list.sort(key = lambda x: x[1], reverse=True)
  columns = [ {"field": esc(k), "headerName": k} for (k,_) in column_list]
  columns_total = {"row_header": "Language", "row_type": "TOTAL"} | { esc(p[0]): p[1] for p in column_list }

  def build_row(k1):
    total = sum(main_dict[k1].values())
    return (
      { "row_header": k1, "row_total": total} 
      | { esc(k2): [main_dict[k1][k2], main_dict[k1][k2]/total] for k2 in main_dict[k1]}
    )
  
  cells = [ build_row (k1) for k1 in main_dict ]

  output = { 
    "kind": "TBC",
    "title": title,
    "timestamp": datetime.datetime.now().isoformat(),
    "grew_match_instance": args.instance,
    "request": text_request,
    "col_key": clustering_key,
    "columns": columns, 
    "columns_total": columns_total,
    "cells": cells,
    "display_modes": [["occ", "NUM"], ["% of row", "PERCENT"]],
  }

  print (json.dumps(output, indent=2))

