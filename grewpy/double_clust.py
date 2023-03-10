import datetime
import sys
import json

from grewpy import Request, Corpus, set_config
set_config('sud')

if __name__ == '__main__':
  corpus_name = sys.argv[1]
  corpus_files = sys.argv[2:]
  corpus = Corpus(corpus_files)

  dc = corpus.count(Request("N[upos = AUX]; e: M -> N"), clustering_keys=["N.lemma", "e.label"])

  columns_dict = dict()
  for k1 in dc:
    for k2 in dc[k1]:
      columns_dict[k2] = dc[k1][k2] + columns_dict.get(k2, 0)
  column_list = [(c, columns_dict[c]) for c in columns_dict]
  column_list.sort(key = lambda x: x[1], reverse=True)
  columns = [ {"field": k, "headerName": k} for (k,_) in column_list]
  columns_total = {"row_header": "TOTAL"} | { p[0]: p[1] for p in column_list }

  cells = [ {"row_header": k1, "row_total": sum(dc[k1].values())} | { k2: [dc[k1][k2]] for k2 in dc[k1]} for k1 in dc]

  final_json = {
      "columns": columns, 
      "columns_total": columns_total, 
      "cells": cells,
      "title": f"## TODO",
      "timestamp": datetime.datetime.now().isoformat(),
      "display_modes": [["occ", "NUM"]], #, ["% of row", "PERCENT"], ["% of col", "PERCENT"]],
      "grew_match": {
        "cell" : "http://universal.grew.fr?corpus=%s&request=pattern{N[upos = AUX]; e: M -> N; N.lemma=\"$$ROW$$\"; e.label=\"$$COL$$\"}" % corpus_name,
        "row" : "http://universal.grew.fr?corpus=%s&request=pattern{N[upos = AUX]; e: M -> N; N.lemma=\"$$ROW$$\"}" % corpus_name,
        "col" : "http://universal.grew.fr?corpus=%s&request=pattern{N[upos = AUX]; e: M -> N; e.label=\"$$COL$$\"}" % corpus_name,
      }
    }
  
  print (json.dumps(final_json, indent=2))
