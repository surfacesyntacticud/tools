import sys
import subprocess
import json
import re
import glob
import os.path
import argparse
from xml.dom.expatbuilder import parseString


# The list of features used in UD 2.10 is needed or generated the right Grew pattern for the MISC case
# See: https://grew.fr/doc/conllu/#how-the-misc-field-is-handled-by-grew
ud_feats_2_10 = [
    "Abbr", "AdjType", "AdpType", "AdvType", "Agglutination", "Analyt", "Animacy", "Animacy[gram]", "Antr", "Aspect", "Augm",
    "Case", "Cfm", "Clas", "Class", "Clitic", "Clusivity", "Clusivity[obj]", "Clusivity[psor]", "Clusivity[subj]", "Compound", "Comt", 
    "ConjType", "Connegative", "Contrast", "Contv", "Corf", "Decl", "Definite", "Definitizer", "Degree", "DegreeModQpm", "Deixis",
    "DeixisRef", "Deixis[psor]", "Delib", "Deo", "Derivation", "Determ", "Detrans", "Dev", "Dialect", "Dimin", "Dist", "Echo", "Emph",
    "Emphatic", "Evident", "Excl", "Foc", "Focus", "FocusType", "Foreign", "Form",
    "Gender", "Gender[dat]", "Gender[erg]", "Gender[obj]", "Gender[psor]", "Gender[subj]", "HebBinyan", "HebExistential", "Hum",
    "Hyph", "Imprs", "Incorp", "InfForm", "InflClass", "InflClass[nominal]", "Int", "Intens", "Intense", "Intension",
    "LangId", "Language", "Link", "Mood", "Morph", "Movement", "Mutation", "NCount", "NameType", "NegationType", "Neutral",
    "Nomzr", "NonFoc", "NounBase", "NounClass", "NounType", "NumForm", "NumType", "NumValue",
    "Number", "Number[abs]", "Number[dat]", "Number[erg]", "Number[obj]", "Number[psed]", "Number[psor]", "Number[subj]",
    "Obl", "Orth", "PartForm", "PartType", "PartTypeQpm", "Pcl",
    "Person", "Person[abs]", "Person[dat]", "Person[erg]", "Person[obj]", "Person[psor]", "Person[subj]",
    "Polarity", "Polite", "Polite[abs]", "Polite[dat]", "Polite[erg]", "Position", "Poss", "Possessed",
    "Pred", "Prefix", "PrepCase", "PrepForm", "Priv", "PronType", "Proper", "Pun", "PunctSide", "PunctType",
    "Recip", "Red", "Redup", "Reflex", "Reflex[obj]", "Reflex[subj]", "Rel", "Report", "Speech", "Strength",
    "Style", "SubGender", "Subcat", "Subordinative", "Tense", "Top", "Trans", "Tv", "Typo", "Uninflect",
    "Valency", "Variant", "Ventive", "VerbClass", "VerbForm", "VerbStem", "VerbType", "Voice",
    "Shared" # SUD
  ]

parser = argparse.ArgumentParser()
parser.add_argument("basedir", help = "the main folder where all corpora are stored as subdirs")
parser.add_argument("columns", help = "Must be one either of the values 'FEATS', 'MISC', 'DEPS' or is interpreted as a feature name")
parser.add_argument("-f", "--filter", help = "The template for selecting treebanks", default="*")
parser.add_argument("-o", "--out_file", help = "The name of the output json file")
parser.add_argument("-s", "--suffix", default="@2.10", help = "The suffix used in Grew-match naming of the corpus")
parser.add_argument("-t", "--title", help = "The title of the final webpage")
parser.add_argument("-q", "--quiet", action="store_true", default = False, help = "turn off the progession info printing")
args=parser.parse_args()

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# ==== Step 1 ====
# Build the list in corpora to consider in [corpus_list]
corpus_list = [os.path.basename(d) for d in glob.glob(args.basedir+"/"+args.filter)]
if (not args.quiet):
    print ("%d corpora found: %s" % (len(corpus_list), str(corpus_list)),file=sys.stderr)

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# ==== Step 2 ====
# Fill [dict] with the ouputs of the unix commands
dict={}
nb_column={}

corpus_cpt = 0

def add_corpus (corpus):
    global corpus_cpt
    corpus_cpt += 1
    sub_dict = {}

    nb_token = int(subprocess.run(['cat %s/%s/*.conllu | egrep "^[.0-9]+\t" | wc -l' % (args.basedir, corpus)], capture_output=True, shell=True, encoding='UTF-8').stdout)
    nb_sent = int(subprocess.run(['cat %s/%s/*.conllu | grep "^# sent_id =" | wc -l' % (args.basedir, corpus)], capture_output=True, shell=True, encoding='UTF-8').stdout)

    if args.columns == "FEATS":
        command = 'cat %s/%s/*.conllu | egrep "^[.0-9]+\t" | cut -f 6 | grep -v "_" | tr "|" "\n" | cut -f 1 -d "=" | sort | uniq -c' % (args.basedir, corpus)
    elif args.columns == "DEPS":
        command = 'cat %s/%s/*.conllu | egrep "^[.0-9]+\t" | cut -f 8 | sort | uniq -c' % (args.basedir, corpus)
    elif args.columns == "MISC":
        command = 'cat %s/%s/*.conllu | egrep "^[.0-9]+\t" | cut -f 10 | tr "|" "\n" | grep "=" | cut -f 1 -d "=" | sort | uniq -c' % (args.basedir, corpus)
        print (command)
    else:
        command = 'cat %s/%s/*.conllu | egrep "^[.0-9]+\t" | cut -f 6 | tr "|" "\n" | grep "^%s=" | cut -f 2 -d "=" | sort | uniq -c' % (args.basedir, corpus, args.columns)
    raw = subprocess.run([command], capture_output=True, shell=True, encoding='UTF-8')
    column_cpt = 0 
    for line in raw.stdout.split("\n"):
        fields = line.strip().split(" ")
        if len(fields) == 2:
            occ = int(fields[0])
            column_cpt += 1
            sub_dict[fields[1]] = (occ, occ/nb_sent, occ/nb_token)
    nb_column[corpus] = column_cpt
    dict[corpus] = sub_dict

for corpus in corpus_list:
    if (not args.quiet):
        print ("---> %d/%d: %s" % (corpus_cpt + 1, len(corpus_list), corpus),file=sys.stderr)
    add_corpus(corpus)

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# ==== Step 3 ====
# build [key_list]: the list of couple (feature_name, nb_of_corpora_using_this_feature), 

# sorted by decreasing order of nb_of_corpora_using_this_feature
# Compute from data in [dict], how many corpora use the feature [feat]
def nb_corpora(feat):
    cpt = 0
    for corpus in dict:
        if feat in dict[corpus]:
            cpt += 1 
    return cpt

# Compute a set [keys] with the union of all corpora keys (will be the columns)
keys = set()
for k in dict:
    keys = keys.union(set(dict[k].keys()))
key_list = [(k,nb_corpora(k)) for k in list(keys)]
key_list.sort(key=lambda k: k[1], reverse=True)

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# ==== Step 4 ====
# Build the final JSON object

# get the value of a cell, with default as 0
def get_occ(corpus, feature):
    sub=dict[corpus]
    return sub.get(feature, 0)

# turn UD notation "Number[psor]" into Grew notation "Number__psor"
def grew_feat_name(f):
    sp = re.split("\[|\]", f)
    return (sp[0]+"__"+sp[1] if len(sp) > 1 else f)

# build the Grew pattern
def pattern_feats (feature):
    grew_feature = grew_feat_name(feature)
    return (['pattern { N [%s] }' % grew_feature], "N.%s" % grew_feature)

# build the Grew pattern
def pattern_misc (feature):
    prefix = "__MISC__" if feature in ud_feats_2_10 else ""
    grew_feature = prefix + grew_feat_name(feature)
    return (['pattern { N [%s] }' % grew_feature], "N.%s" % grew_feature)

def pattern_deps (dep):
    return (['pattern {M -[%s]-> N}' %dep], None)

def pattern_feat (feat_name, feat_value):
    return (['pattern { N [%s="%s"] }' % (grew_feat_name(feat_name), feat_value)], None)

def pattern (x):
    if args.columns == "FEATS":
        return pattern_feats(x)
    elif args.columns == "DEPS":
        return pattern_deps(x)
    elif args.columns == "MISC":
        return pattern_misc(x)
    else:
        return pattern_feat(args.columns, x)

def default_title (x):
    if args.columns == "FEATS":
        return "## Usage of features in `FEATS` CoNLL column"
    elif args.columns == "MISC":
        return "## Usage of features in `MISC` CoNLL column (see [Grew doc](https://grew.fr/doc/conllu/#how-the-misc-field-is-handled-by-grew))"
    elif args.columns == "DEPS":
        return "## Usage of dependency relations"
    else:
        return "## Usage of `%s` feature" % (args.columns)

def build_row(corpus):
    d = dict[corpus]
    d.update({"treebank": corpus+args.suffix})
    return d

grid = {
    "title": "## " + args.title if args.title != None else default_title(args.columns),
    "grew_match": 
        {feat: {
            "code": pattern(feat)[0], 
            "key": pattern(feat)[1], 
            "users": users}
        for (feat, users) in key_list },
    "columns": [{"field": feat, "headerName": feat} for (feat, users) in key_list],
    "cells": [build_row(corpus) for corpus in corpus_list]
}

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# ==== Step 5 ====
# Store the final JSON object in a file
if args.out_file == None:
    json.dump(grid, sys.stdout, indent=2)
else:
    with open(args.out_file, "w") as file:
        json.dump(grid, file, indent=2)
