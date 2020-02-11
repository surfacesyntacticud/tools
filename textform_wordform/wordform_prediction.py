#! /usr/bin/env python
import sys

def add_feat (feats,new_feat):
    if feats == "_":
        feat_list = []
    else:
        feat_list = feats.split("|")
    new_list = feat_list + [new_feat]
    sorted_list = new_list.sort(key=lambda x: x.lower())
    return ("|".join(new_list))

def add_wordform (infile, outfile):
    with open(infile, 'r') as input:
        with open(outfile, 'w') as output:
            for line in input:
                line = line.rstrip()
                if (line != "") and (line[0] != '#'):
                    fields = line.split("\t")
                    if fields[3] != "PROPN":
                        l = fields[1].lower()
                        if l != fields[1]:
                            fields[9] = add_feat(fields[9], "wordform="+l)
                            line = "\t".join(fields)
                output.write (line+"\n")

if len(sys.argv) == 3:
    add_wordform(sys.argv[1],sys.argv[2])
else:
    print ("Usage: wordform_predication.py <infile> <outfile>")
