import datetime
import sys
import json

from grewpy import Request, Corpus, set_config
set_config('sud')

if __name__ == '__main__':
  corpus_name = sys.argv[1]
  corpus_files = sys.argv[2:]
  corpus = Corpus(corpus_files)

  base_request = "e: M -> N"
  row_key = "N.upos"
  col_key = "e.label"

  dc = corpus.count(Request(base_request), clustering_keys=[row_key, col_key])

  columns_dict = dict()
  for k1 in dc:
    for k2 in dc[k1]:
      columns_dict[k2] = dc[k1][k2] + columns_dict.get(k2, 0)
  column_list = [(c, columns_dict[c]) for c in columns_dict]
  column_list.sort(key = lambda x: x[1], reverse=True)
  columns = [ {"field": k, "headerName": k} for (k,_) in column_list]
  columns_total = {"row_header": "TOTAL_ROW"} | { p[0]: p[1] for p in column_list }

  cells = [ {"row_header": k1, "row_total": sum(dc[k1].values())} | { k2: [dc[k1][k2]] for k2 in dc[k1]} for k1 in dc]

  final_json = {
      "title": f"## TODO",
      "base_request": base_request,
      "row_key": row_key,
      "col_key": col_key,
      "timestamp": datetime.datetime.now().isoformat(),
      "display_modes": [["occ", "NUM"]], #, ["% of row", "PERCENT"], ["% of col", "PERCENT"]],
      "columns": columns, 
      "columns_total": columns_total, 
      "cells": cells,
      "grew_match": {
        "cell" : "http://universal.grew.fr?corpus=%s&request=pattern{%s} with {%s=\"$$ROW$$\"; %s=\"$$COL$$\"}" % (corpus_name, base_request, row_key, col_key),
        "row" : "http://universal.grew.fr?corpus=%s&request=pattern{%s} with {%s=\"$$ROW$$\"}" % (corpus_name, base_request, row_key),
        "col" : "http://universal.grew.fr?corpus=%s&request=pattern{%s} with {%s=\"$$COL$$\"}" % (corpus_name, base_request, col_key),
      }
    }
  
  print (json.dumps(final_json, indent=2))
