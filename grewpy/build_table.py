import sys
import argparse
import json
import datetime
from grewpy import Request, Corpus, set_config

parser = argparse.ArgumentParser(description="Build a Grew table from a list of treebanks and a list of requests")
parser.add_argument("kind", help="the kind of table to build: TBR (treebanks/requests) or TBC (treebanks/clustering)")
parser.add_argument("--treebanks", help="a JSON file with the list of treebanks")
parser.add_argument("--treebank", help="[DC only] a JSON string: dict from id to treebank")
parser.add_argument("--requests", help="[TBR only] a JSON file with the list of requests")
parser.add_argument("--request", help="[TBC only] a JSON file with the main request")
parser.add_argument("--clustering_key", help="[TBC only] the key used for clustering")
parser.add_argument("--col_key", help="[TBC only] the key used for col")
parser.add_argument("--row_key", help="[TBC only] the key used for row")
parser.add_argument("-i", "--instance", help="grew-match instance", default="https://universal.grew.fr")
parser.add_argument("-t", "--title", help="title of the table (markdown)")
parser.add_argument("-c", "--config", help="grew config")
parser.add_argument('-f', '--filter', help="Remove lines with only one non zero column", action='store_true')
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

def treebanks():
  if args.kind in ["TBR", "TBC"] and args.treebanks:
    with open(args.treebanks, "rb") as f:
      return json.load(f)
  else:
    print (f"Missing --treebanks", file=sys.stderr)
    raise ValueError

def request_of_json (data):
  grew_request = Request.from_json(data["request"])
  text = str(grew_request)
  if "comment" in data:
    text_request = f'{data["comment"].replace("%", "%25")}\n{text}'.replace("\n", "%0A")
  else:
    text_request = f'{text}'.replace("\n", "%0A")
  return (grew_request, text_request)

# ===============================================================================================
# Table with several treebanks and several requests
# ===============================================================================================
if __name__ == '__main__' and args.kind == "TBR":
  with open(args.requests, "rb") as f:
    data_requests = json.load(f)
  grew_requests = dict()
  text_requests = dict()
  for id in data_requests:
    (grew_request, text_request) = request_of_json (data_requests[id])
    grew_requests[id] = grew_request
    text_requests[id] = text_request

  corpora = treebanks()
  main_dict = {}
  for corpus_id in corpora:
    corpus = Corpus(corpora[corpus_id])
    full_dict = { id: corpus.count(grew_requests[id]) for id in grew_requests }
    main_dict[corpus_id] = { id: full_dict[id] for id in full_dict if full_dict[id]>0 }
    corpus.clean()

  columns = [ {"field": id, "headerName": id} for id in grew_requests]
  # columns_total = {"row_header": "Treebank", "row_type": "TOTAL"} | { id: sum([main_dict[corpus_id].get(id,0) for corpus_id in corpora]) for id in grew_requests }
  columns_total = { id: sum([main_dict[corpus_id].get(id,0) for corpus_id in corpora]) for id in grew_requests }
  columns_total["row_header"] = "Treebank"
  columns_total["row_type"] = "TOTAL"

  def build_row(k1):
    d = { k2: [main_dict[k1].get(k2,0)] for k2 in main_dict[k1]}
    d["row_header"] = k1
    d["row_total"] = sum(main_dict[k1].values())
    return d
  cells = [ build_row (k1) for k1 in main_dict]

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

# ===============================================================================================
# Table with several treebanks one request and a clustering_key
# ===============================================================================================
if __name__ == '__main__' and args.kind == "TBC":

  if args.request:
    with open(args.request, "rb") as f:
      data = json.load(f)
      (grew_request, text_request) = request_of_json (data)
  else:
    print (f"Missing --request", file=sys.stderr)
    raise ValueError

  if args.clustering_key:
    clustering_key = args.clustering_key
  else:
    print (f"Missing --clustering_key", file=sys.stderr)
    raise ValueError

  corpora = treebanks()
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
  columns_total = { esc(p[0]): p[1] for p in column_list }
  columns_total["row_header"] = "Language"
  columns_total["row_type"] = "TOTAL"

  def build_row(k1):
    total = sum(main_dict[k1].values())
    d = { esc(k2): [main_dict[k1][k2], main_dict[k1][k2]/total] for k2 in main_dict[k1]}
    d["row_header"] = k1
    d["row_total"] = total
    return d 
  
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



# ===============================================================================================
# Table with one treebank, one request and a two clustering
# ===============================================================================================
if __name__ == '__main__' and args.kind == "DC":
  if args.request:
    with open(args.request, "rb") as f:
      data = json.load(f)
      (grew_request, text_request) = request_of_json (data)
  else:
    print (f"Missing --request", file=sys.stderr)
    raise ValueError

  if args.row_key:
    row_key = args.row_key
  else:
    print (f"Missing --row_key", file=sys.stderr)
    raise ValueError
  if args.col_key:
    col_key = args.col_key
  else:
    print (f"Missing --col_key", file=sys.stderr)
    raise ValueError

  if args.treebank:
    data = json.loads(args.treebank)
    (treebank_id, treebank_loc) = data.popitem()
    corpus=Corpus(treebank_loc)
  else:
    print (f"Missing --treebank", file=sys.stderr)
    raise ValueError

  dc_full = corpus.count(grew_request, clustering_keys=[row_key, col_key])
  if args.filter:
    dc = { k: dc_full[k] for k in dc_full if len(dc_full[k]) > 1 }
  else:
    dc = dc_full

  columns_dict = dict()
  for k1 in dc:
    for k2 in dc[k1]:
      columns_dict[k2] = dc[k1][k2] + columns_dict.get(k2, 0)
  column_list = [(c, columns_dict[c]) for c in columns_dict]
  column_list.sort(key = lambda x: x[1], reverse=True)
  columns = [ {"field": k, "headerName": k} for (k,_) in column_list]
  columns_total = { p[0]: p[1] for p in column_list }
  columns_total["row_header"] = row_key
  columns_total["row_type"] = "TOTAL"

  def build_row(k1):
    d = { k2: [dc[k1][k2]] for k2 in dc[k1]}
    d["row_header"] = k1
    d["row_total"] = sum(dc[k1].values())
    return d
  cells = [ build_row (k1) for k1 in main_dict]

  final_json = {
      "kind": "DC",
      "title": title,
      "timestamp": datetime.datetime.now().isoformat(),
      "grew_match_instance": args.instance,
      "request": text_request,
      "treebank": treebank_id,
      "col_key": col_key,
      "row_key": row_key,
      "columns": columns, 
      "columns_total": columns_total, 
      "cells": cells,
      "display_modes": [["occ", "NUM"]], #, ["% of row", "PERCENT"], ["% of col", "PERCENT"]]
    }
  
  print (json.dumps(final_json, indent=2))
