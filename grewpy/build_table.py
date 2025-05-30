import os
import sys
import argparse
import json
import datetime
from grewpy import Request, Corpus, set_config
import re
import glob

def replace_env_variables(input_string):
    # Define a regex pattern to match the format ${VAR}
    pattern = r'\$\{(\w+)\}'
    
    # Function to replace matched variable with its environment value
    def replace_variable(match):
        var_name = match.group(1)  # Extract the variable name
        return os.getenv(var_name)  # Return the value or empty string if not found

    # Use re.sub to replace all occurrences of the pattern
    result = re.sub(pattern, replace_variable, input_string)
    return result



def treebanks(args):
  if args.kind in ["TBR", "TBC"] and args.treebanks:
    with open(args.treebanks, "rb") as f:
      data = json.load(f)
      return data
  else:
    raise ValueError(f"Missing --treebanks")

def request_of_json (data):
  grew_request = Request.from_json(data["request"])
  text = str(grew_request)
  if "comment" in data:
    text_request = f'{data["comment"].replace("%", "%25")}\n{text}'.replace("\n", "%0A")
  else:
    text_request = f'{text}'.replace("\n", "%0A")
  return (grew_request, text_request)

def load_corpus (corpus_desc):
  corpus_id = corpus_desc["id"]
  directory = replace_env_variables(corpus_desc["directory"])
  if "files" in corpus_desc:
    if isinstance (corpus_desc["files"], str):
      full_names = glob.glob(f'{directory}/*{corpus_desc["files"]}')
    else:
      full_names = [os.path.join(directory, file) for file in corpus_desc["files"]]
    return (corpus_id, Corpus(full_names))
  else:
    return (corpus_id, Corpus (directory))


# ===============================================================================================
# Table with several treebanks and several requests
# ===============================================================================================
def table_TBR(args):
  title = args.title if args.title else "## Table treebanks/request"
  with open(args.requests, "rb") as f:
    data_requests = json.load(f)
  grew_requests = dict()
  text_requests = dict()
  for id, request in data_requests.items():
    (grew_request, text_request) = request_of_json (request)
    grew_requests[id] = grew_request
    text_requests[id] = text_request

  corpora = treebanks(args)
  size = len(corpora)
  main_dict = {}
  for corpus_desc in corpora:
    print (f'[{len(main_dict)+1}/{size}] -> {corpus_desc["id"]}', file=sys.stderr)
    (corpus_id, corpus) = load_corpus (corpus_desc)
    full_dict = { id: corpus.count(grew_requests[id]) for id in grew_requests }
    main_dict[corpus_id] = { id: full_dict[id] for id in full_dict if full_dict[id]>0 }
    corpus.clean()

  columns = [ {"field": id, "headerName": id} for id in grew_requests]
  # columns_total = {"row_header": "Treebank", "row_type": "TOTAL"} | { id: sum([main_dict[corpus_id].get(id,0) for corpus_id in corpora]) for id in grew_requests }
  columns_total = { id: sum([main_dict[corpus_desc["id"]].get(id,0) for corpus_desc in corpora]) for id in grew_requests }
  if args.total:
    columns_total["row_total"] = sum (columns_total.values())
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
    "grew_match_instance": args.instance,
    "requests": text_requests,
    "col_key": "Request",
    "columns": columns, 
    "columns_total": columns_total, 
    "cells": cells,
    "display_modes": [["occ", "NUM"]],
  }

  if args.timestamp:
    output["timestamp"] = datetime.datetime.now().isoformat()

  if args.home:
    output["home"] = args.home

  if args.output:
    with open(args.output, 'w') as f:
      json.dump(output, f)
  else:
    print (json.dumps(output, indent=2))

# ===============================================================================================
# Table with several treebanks one request and a clustering_key
# ===============================================================================================
def table_TBC(args):
  title = args.title if args.title else "## Table treebanks/clustering"
  if args.request:
    if args.request.endswith(".json"):
      with open(args.request, "rb") as f:
        data = json.load(f)
        (grew_request, text_request) = request_of_json (data)
    else:
      grew_request = Request(args.request)
      text_request = args.request
  else:
    raise ValueError(f"Missing --request")

  if args.clustering_key:
    clustering_key = args.clustering_key
  else:
    raise ValueError(f"Missing --clustering_key")

  corpora = treebanks(args)
  main_dict = {}
  for corpus_desc in corpora:
    (corpus_id, corpus) = load_corpus (corpus_desc)
    main_dict[corpus_id] = corpus.count(grew_request, clustering_keys=[clustering_key])
    print(f"[{len(main_dict)}/{len(corpora)}] {corpus_id} done", file=sys.stderr)
    corpus.clean()

  def esc(s):
    return s.replace(".", "_")

  columns_dict = dict()
  for corpus_id in main_dict:
    if main_dict[corpus_id] == 0:
      pass
    else:
      for k2 in main_dict[corpus_id]:
        columns_dict[k2] = main_dict[corpus_id][k2] + columns_dict.get(k2, 0)
  column_list = [(c, columns_dict[c]) for c in columns_dict]
  column_list.sort(key = lambda x: x[1], reverse=True)
  columns = [ {"field": esc(k), "headerName": k} for (k,_) in column_list]
  columns_total = { esc(p[0]): p[1] for p in column_list }
  columns_total["row_header"] = "Language"
  columns_total["row_type"] = "TOTAL"
  if args.total:
    columns_total["row_total"] = sum(columns_dict.values())

  def build_row(k1):
    if main_dict[k1] == 0:
      total = 0
      d = {}
    else:
      total = sum(main_dict[k1].values())
      d = { esc(k2): [main_dict[k1][k2], main_dict[k1][k2]/total] for k2 in main_dict[k1]}
    d["row_header"] = k1
    d["row_total"] = total
    return d 
  
  cells = [ build_row (k1) for k1 in main_dict ]

  output = { 
    "kind": "TBC",
    "title": title,
    "grew_match_instance": args.instance,
    "request": text_request,
    "col_key": clustering_key,
    "columns": columns, 
    "columns_total": columns_total,
    "cells": cells,
    "display_modes": [["occ", "NUM"], ["% of row", "PERCENT"]],
  }

  if args.timestamp:
    output["timestamp"] = datetime.datetime.now().isoformat()

  if args.home:
    output["home"] = args.home

  if args.output:
    with open(args.output, 'w') as f:
      json.dump(output, f)
  else:
    print (json.dumps(output, indent=2))


# ===============================================================================================
# Table with one treebank, one request and a two clustering
# ===============================================================================================
def table_DC(args):
  title = args.title if args.title else "## Table double clustering"
  if args.request:
    if args.request.endswith(".json"):
      with open(args.request, "rb") as f:
        data = json.load(f)
        (grew_request, text_request) = request_of_json (data)
    else:
      grew_request = Request(args.request)
      text_request = args.request
  else:
    raise ValueError(f"Missing --request")

  if args.row_key:
    row_key = args.row_key
  else:
    raise ValueError(f"Missing --row_key")
  if args.col_key:
    col_key = args.col_key
  else:
    raise ValueError(f"Missing --col_key")

  if args.treebank:
    data = json.loads(args.treebank)
    (treebank_id, treebank_loc) = data.popitem()
    corpus=Corpus(treebank_loc)
  else:
    raise ValueError(f"Missing --treebank")

  dc_full = corpus.count(grew_request, clustering_keys=[row_key, col_key])
  if dc_full == 0: # The pattern does not appear in the corpus
    return
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
  if args.total:
    columns_total["row_total"] = sum (columns_total.values())
  columns_total["row_header"] = row_key
  columns_total["row_type"] = "TOTAL"

  def build_row(k1):
    d = { k2: [dc[k1][k2]] for k2 in dc[k1]}
    d["row_header"] = k1
    d["row_total"] = sum(dc[k1].values())
    return d
  cells = [ build_row (k1) for k1 in dc]

  final_json = {
      "kind": "DC",
      "title": title,
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

  if args.timestamp:
    final_json["timestamp"] = datetime.datetime.now().isoformat()

  if args.home:
    final_json["home"] = args.home

  if args.output:
    with open(args.output, 'w') as f:
      json.dump(final_json, f)
  else:
    print (json.dumps(final_json, indent=2))

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Build a Grew table from a list of treebanks and a list of requests")
  parser.add_argument("kind", help="the kind of table to build: TBR (treebanks/requests), TBC (treebanks/clustering) or DC (double clustering)")
  parser.add_argument("--treebanks", help="a JSON file with the list of treebanks")
  parser.add_argument("--treebank", help="[DC only] a JSON string: dict from id to treebank")
  parser.add_argument("--requests", help="[TBR only] a JSON file with the list of requests")
  parser.add_argument("--request", help="[TBC only] a JSON file with the main request")
  parser.add_argument("--clustering_key", help="[TBC only] the key used for clustering")
  parser.add_argument("--col_key", help="[TBC only] the key used for col")
  parser.add_argument("--row_key", help="[TBC only] the key used for row")
  parser.add_argument("--output", help="output file (default is stdout)")
  parser.add_argument("--home", help="url to the 'home' page")
  parser.add_argument('--timestamp', help="Add a timestamp on table", action='store_true')
  parser.add_argument('--total', help="Print grand total", action='store_true')
  parser.add_argument("-i", "--instance", help="grew-match instance", default="https://universal.grew.fr")
  parser.add_argument("-t", "--title", help="title of the table (markdown)")
  parser.add_argument("-c", "--config", help="grew config")
  parser.add_argument('-f', '--filter', help="Remove lines with only one non zero column", action='store_true')
  args = parser.parse_args()

  if args.config:
    set_config(args.config)

  match args.kind:
    case "TBR":
      table_TBR(args)
    case "TBC":
      table_TBC(args)
    case "DC":
      table_DC(args)
    case _:
      raise ValueError(f"Unknown kind {args.kind}")
