import datetime
import argparse
import sys
import json
from grewpy import CorpusDraft, Request, Corpus, set_config

parser = argparse.ArgumentParser(description="Build a Grew table listing features by UPOS")
parser.add_argument("--treebank", help="a JSON string: dict from id to treebank")
parser.add_argument("--output", help="output file (default is stdout)")
parser.add_argument("-i", "--instance", help="grew-match instance", default="https://universal.grew.fr")
parser.add_argument("-c", "--config", help="grew config")
args = parser.parse_args()

if args.config:
  set_config(args.config)

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
  elif f in ['SpaceAfter', 'Shared', 'Typo', 'Title', 'InTitle', 'Idiom', 'InIdiom', '__RAW_MISC__']:
    # Feature not related to POS of the token
    return False
  elif f.startswith('Syl'):
    # Feature used of syllables in Naija-prosody
    return False
  else:
    # Keep everthing else
    return True

# change xx__yy to xx[yy]
def feat_name_grew2ud (s):
  sp = s.split("__")
  if len(sp) == 2:
    return f"{sp[0]}[{sp[1]}]"
  else:
    return s

def build_table (rows, columns, cell_fct, row_fct, col_fct):
  columns_dict = [ {"field": column, "headerName": feat_name_grew2ud(column)} for column in columns ]
  columns_total_dict =  {"row_header": "upos", "row_type": "TOTAL"} | { column: col_fct (column) for column in columns }
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
  if args.treebank:
    data = json.loads(args.treebank)
    (treebank_id, treebank_loc) = data.popitem()
    corpus=Corpus(treebank_loc)
  else:
    print (f"Missing --treebank", file=sys.stderr)
    raise ValueError

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
    return corpus.count(Request(f'pattern {{X[upos={upos}, {feat}]}}'))
  def row_fct(upos):
    return corpus.count(Request(f'pattern {{X[upos={upos}]}}'))
  def col_fct(feat):
    return corpus.count(Request(f'pattern {{X[{feat}]}}'))
  table = build_table(ud_tagset, features, cell_fct, row_fct, col_fct)
  table.update ({
    "kind": "DC",
    "title": f"## Usage of features by UPOS in `{treebank_id}` (master)",
    "timestamp": datetime.datetime.now().isoformat(),
    "grew_match_instance": args.instance,
    "request": "pattern { X [] }",
    "treebank": treebank_id,
    "col_key": "X.__feature_name__",
    "row_key": "X.upos",
    "display_modes": [["occ", "NUM"], ["% of row", "PERCENT"], ["% of col", "PERCENT"]]
  })

  if args.output:
    with open(args.output, 'w') as f:
      json.dump(table, f)
  else:
    print (json.dumps(table, indent=2))
