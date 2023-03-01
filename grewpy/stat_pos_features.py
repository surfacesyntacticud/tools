import sys
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

if __name__ == '__main__':
  corpus_files = sys.argv[1:]
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

  # print the table in Markdown syntax
  print (' |  | '+ ' | '.join(features))
  print ('|---|'+ '---|' * len(features))
  for upos in ud_tagset:
    print (f' | {upos} ', end='')
    total = corpus.count(Request(f'N[upos={upos}]'))
    for feat in features:
      yes = corpus.count(Request(f'N[upos={upos}, {feat}]'))
      if yes == 0:
        print (' | ', end='')
      else: 
        print (' | %.2f%%' % (yes/total*100), end='')
    print()

