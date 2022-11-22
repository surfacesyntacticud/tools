import unicodedata
import sys

infile = sys.argv[1]

with open(infile) as f:
    lines = f.readlines()

for l in lines:
  print (unicodedata.normalize('NFC', l.strip()))
 
