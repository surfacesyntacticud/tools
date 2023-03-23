import datetime
import sys
import json

from grewpy import Request, Corpus, set_config
set_config('sud')

def req_of_key(key, dir):
  if "#" in key:
    return "with {$$%s$$}" % dir
  else:
    return "with {%s = \"$$%s$$\"}" % (key,dir)

if __name__ == '__main__':
  requests = sys.argv[1]
  corpus_name = sys.argv[2]
  corpus_files = sys.argv[3:]
  corpus = Corpus(corpus_files)

  if requests == "adj_lemma_pos":
    # ---------------- adj_lemma_pos -----------------
    title = f"## adj lemma position ({corpus_name})"
    base_request = "e: N -[mod]-> A; A[upos=ADJ]"
    row_key = "A.lemma"
    col_key = "N#A"
    filter_uniline = False

  elif requests == "label_upos":
    # ---------------- label_upos -----------------
    title = f"## edge label and dependant UPOS ({corpus_name})"
    base_request = "e: M -> N"
    row_key = "e.label"
    col_key = "N.ExtPos/upos"
    filter_uniline = False

  elif requests == "amb_lemma":
  # ---------------- amb_lemma -----------------
    title = f"## ambiguous lemmas UPOS ({corpus_name})"
    base_request = "N[lemma]"
    row_key = "N.lemma"
    col_key = "N.upos"
    filter_uniline = True

  elif requests == "aux_lemma_label":
  # ---------------- aux_lemma_label -----------------
    title = f"## AUX: lemmas / label ({corpus_name})"
    base_request = "N[upos = AUX]; e: M -> N"
    row_key = "N.lemma"
    col_key = "e.label"
    filter_uniline = False

  else:
    print (f"Unknown test {requests}")


  dc_full = corpus.count(Request(base_request), clustering_keys=[row_key, col_key])

  if filter_uniline:
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
  columns_total = {"row_header": row_key, "row_type": "TOTAL_SEARCH"} | { p[0]: p[1] for p in column_list }

  cells = [ {"row_header": k1, "row_total": sum(dc[k1].values())} | { k2: [dc[k1][k2]] for k2 in dc[k1]} for k1 in dc]

  final_json = {
      "title": title,
      "base_request": base_request,
      "row_key": row_key,
      "col_key": col_key,
      "timestamp": datetime.datetime.now().isoformat(),
      "display_modes": [["occ", "NUM"]], #, ["% of row", "PERCENT"], ["% of col", "PERCENT"]],
      "columns": columns, 
      "columns_total": columns_total, 
      "cells": cells,
      "grew_match": {
        "cell" : "http://universal.grew.fr?corpus=%s&request=pattern{%s} %s %s" % (corpus_name, base_request, req_of_key(row_key, "ROW"), req_of_key(col_key, "COL")),
        "row" : "http://universal.grew.fr?corpus=%s&request=pattern{%s} %s" % (corpus_name, base_request, req_of_key(row_key, "ROW")),
        "col" : "http://universal.grew.fr?corpus=%s&request=pattern{%s} %s" % (corpus_name, base_request, req_of_key(col_key, "COL")),
      }
    }
  
  print (json.dumps(final_json, indent=2))

