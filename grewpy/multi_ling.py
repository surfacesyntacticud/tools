import datetime
import sys
import json
from grewpy import CorpusDraft, Request, Corpus, set_config
set_config('sud')

parseme_languages = [ "AR", "BG" ]
# parseme_languages = [ "AR", "BG", "CS", "DE", "EL", "EN", "ES", "EU", "FA", "FR", "GA", "HE", "HI", "HR", "HU", "IT", "LT", "MT", "PL", "PT", "RO", "SL", "SR", "SV", "TR", "ZH" ]

def esc(s):
  return s.replace(".", "_")

base_dir = "/Users/guillaum/gitlab/parseme/release-data-dev/1.3/preliminary-release-data"

if __name__ == '__main__':

  main_dict = {}
  for lang in parseme_languages:
    corpus_name = f"PARSEME-{lang}@master"
#    corpus = Corpus([f"{base_dir}/{lang}/dev.cupt", f"{base_dir}/{lang}/test.cupt", f"{base_dir}/{lang}/train.cupt"])
    corpus = Corpus([ f"{base_dir}/{lang}/test.cupt"])
    col_key = "N.label"
    main_dict[lang]  = corpus.count(Request(f'N[label <> NotMWE]'), clustering_keys=[col_key])
    corpus.clean()

  columns_dict = dict()
  for lang in main_dict:
    for k2 in main_dict[lang]:
      columns_dict[k2] = main_dict[lang][k2] + columns_dict.get(k2, 0)
  column_list = [(c, columns_dict[c]) for c in columns_dict]
  column_list.sort(key = lambda x: x[1], reverse=True)
  columns = [ {"field": esc(k), "headerName": k} for (k,_) in column_list]
  columns_total = {"row_header": "Language", "row_type": "TOTAL_ROW"} | { esc(p[0]): p[1] for p in column_list }

  cells = [ {"row_header": k1, "row_total": sum(main_dict[k1].values())} | { esc(k2): [main_dict[k1][k2]] for k2 in main_dict[k1]} for k1 in main_dict]

  all = { 
    "columns": columns, 
    "columns_total": columns_total, 
    "cells": cells,
    "col_key": col_key,
    "title": f"## Parseme MWE by labels",
    "timestamp": datetime.datetime.now().isoformat(),
    # "display_modes": [["occ", "NUM"], ["% of row", "PERCENT"], ["% of col", "PERCENT"]],
    "display_modes": [["occ", "NUM"]],
    "grew_match": {
      "cell" : "http://parseme.grew.fr?corpus=PARSEME-$$ROW$$@master&request=pattern{N [label=\"$$COL$$\"]}",
      "row" : "http://parseme.grew.fr?corpus=PARSEME-$$ROW$$@master&request=pattern{N [label]}",
      "col": "",
    }
  }

  print (json.dumps(all, indent=2))

