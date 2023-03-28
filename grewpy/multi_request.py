import datetime
import sys
import json
from grewpy import Request, Corpus, set_config
set_config('sud')

corpora = {
  "SUD_French-GSD@latest": ["SUD_French-GSD/fr_gsd-sud-test.conllu"],
  "SUD_French-ParisStories@latest": ["SUD_French-ParisStories/ParisStories_2022_lesParentsInconnus.conllu"],
  "SUD_French-Rhapsodie@latest": ["SUD_French-Rhapsodie/fr_rhapsodie.sud.test.conllu"],
}

requests = {
  "nom_subj": "V -[subj]-> N; N[upos=NOUN|PROPN]",
  "pron_subj": "V -[subj]-> N; N[upos=PRON]",
  "other_subj": "V -[subj]-> N; N[upos<>NOUN|PROPN|PRON]",
}

grew_requests = { id: Request(requests[id]) for id in requests}

if __name__ == '__main__':
  main_dict = {}
  for corpus_name in corpora:
    corpus = Corpus(corpora[corpus_name])

    col_key = "Request"
    main_dict[corpus_name] = { id: corpus.count(grew_requests[id]) for id in grew_requests }
    corpus.clean()

  columns = [ {"field": id, "headerName": id, "grew": requests[id]} for id in grew_requests]
  columns_total = {"row_header": "Treebank", "row_type": "TOTAL"} | { id: sum([main_dict[corpus_name][id] for corpus_name in corpora]) for id in grew_requests }

  cells = [ {"row_header": k1, "row_total": sum(main_dict[k1].values())} | { k2: [main_dict[k1][k2]] for k2 in main_dict[k1]} for k1 in main_dict]

  data = { 
    "columns": columns, 
    "columns_total": columns_total, 
    "cells": cells,
    "col_key": col_key,
    "title": f"## `subj` in French SUD",
    "timestamp": datetime.datetime.now().isoformat(),
    # "display_modes": [["occ", "NUM"], ["% of row", "PERCENT"], ["% of col", "PERCENT"]],
    "display_modes": [["occ", "NUM"]],
    "grew_match": {
      "cell" : "http://universal.grew.fr?corpus=__ROW__&request=pattern{__COL__}",
    }
  }

  print (json.dumps(data, indent=2))
