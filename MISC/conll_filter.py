# Python script used to filter a corpus based on a sent_id list
# used to produced train/dev/test split needed in UD release
# Three arguments are needed:
# arg 1: a file which contains the sent_id list (on sent_id by line)
# arg 2: the input corpus
# arg 3: the file where the output is stored

import sys
from conllup.conllup import readConlluFile, writeConlluFile

if len(sys.argv) != 4:
  print ('need three args')
  exit (1)

with open(sys.argv[1]) as f:
  ids = f.readlines()

in_corpus = readConlluFile(sys.argv[2])
dict_corpus = { s['metaJson']['sent_id']: s for s in in_corpus }

out_corpus = [dict_corpus [sent_id.rstrip()] for sent_id in ids]
writeConlluFile(sys.argv[3], out_corpus, overwrite=True)

