import datetime
import sys
import json
from grewpy import CorpusDraft, Request, Corpus, set_config
set_config('sud')

ud_tagset = [
    'ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 
    'INTJ', 'NOUN', 'NUM', 'PART', 'PRON', 'PROPN', 
    'PUNCT', 'SCONJ', 'SYM', 'VERB', 'X'
    ]

def keep (f):
  '''
  decide which features should be kept in the final table
  '''
  if f.startswith('Correct') or f.startswith('Align'):
    # Remove features related to errors of sound alignment
    return False
  elif f.lower() == f:
    # Remove 'special' features form, lemma, upos, xpos, wordform and textform
    return False
  elif f in ['SpaceAfter', 'Title', 'InTitle', 'Idiom', 'InIdiom', '__RAW_MISC__']:
    # Feature not related to POS of the token
    return False
  else:
    # Keep everthing else
    return True

def escape_feat_name (s):
  sp = s.split("__")
  if len(sp) == 2:
    return f"{sp[0]}[{sp[1]}]"
  else:
    return s

def build_table (rows, columns, cell_fct, row_fct, col_fct):
  columns_dict = [ {"field": column, "headerName": escape_feat_name(column), "grew": column} for column in columns ]
  columns_total_dict =  {"row_header": "upos", "row_type": "TOTAL"}  | { column: col_fct (column) for column in columns }
  def line(row):
    row_total = row_fct (row)
    d = {"row_header": row, "row_total": row_total }
    for column in columns:
      occ = cell_fct(row, column)
      if occ > 0:
        d.update({column: [occ, occ / row_total, occ / columns_total_dict[column]]})
    return d
  cells_dict = [ line(row) for row in rows ]
  return { 
    "columns": columns_dict, 
    "columns_total": columns_total_dict, 
    "cells": cells_dict 
  }

if __name__ == '__main__':
  corpus_name = sys.argv[1]
  corpus_files = sys.argv[2:]
  corpus = Corpus(corpus_files)

  # NB: we have to iterate on all graph -> CorpusDraft is much more efficient for this
  corpus_draft = CorpusDraft(corpus)
  all_features = set()
  # collect all features names used in the Treebank
  for sent_id in corpus_draft:
    graph = corpus_draft[sent_id]
    for gid in graph.features:
      fs = graph.features[gid]
      for feat_name in fs:
        all_features.add (feat_name)

  # keep only interesting ones
  features = [f for f in list(all_features) if keep (f)]
  features.sort()

  def cell_fct(upos,feat): 
    return corpus.count(Request(f'N[upos={upos}, {feat}]'))
  def row_fct(upos):
    return corpus.count(Request(f'N[upos={upos}]'))
  def col_fct(feat):
    return corpus.count(Request(f'N[{feat}]'))
  table = build_table(ud_tagset, features, cell_fct, row_fct, col_fct)
  table.update ({
    "title": f"## Usage of features by UPOS in `{corpus_name}` (master)",
    "timestamp": datetime.datetime.now().isoformat(),
    "col_key": "feature",
    "display_modes": [["occ", "NUM"], ["% of row", "PERCENT"], ["% of col", "PERCENT"]],
    "grew_match": {
      "cell" : "http://universal.grew.fr?corpus=%s@latest&request=pattern{N [upos=__ROW__, __COL__]}" % corpus_name,
      "row" : "http://universal.grew.fr?corpus=%s@latest&request=pattern{N [upos=__ROW__]}" % corpus_name,
      "col": "http://universal.grew.fr?corpus=%s@latest&request=pattern{N [__COL__]}" % corpus_name
    }
  })

  print (json.dumps(table, indent=2))
