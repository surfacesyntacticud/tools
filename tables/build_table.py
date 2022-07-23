import subprocess
import json
import re
import glob
import os.path
import sys


# The list of features used in UD 2.10 is needed or generated the right Grew pattern for the MISC case
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

verbose = True

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# Parameters
basedir = "/users/guillaum/resources/sud-treebanks-v2.10"
version = "2.10"
filter = "SUD_*"
col = "DEPS"  # Should be "FEATS", "MISC" or "DEPS"
out_file = "sud_deps.json"

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# ==== Step 1 ====
# Build the list in corpora to consider in [corpus_list]
corpus_list = [os.path.basename(d) for d in glob.glob(basedir+"/"+filter)]
if verbose:
    print ("%d corpora found: %s" % (len(corpus_list), str(corpus_list)))

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# ==== Step 2 ====
# Fill [dict] with the ouputs of the unix commands
dict={}
nb_col={}

corpus_cpt = 0

def add_corpus (corpus):
    global corpus_cpt
    corpus_cpt += 1
    sub_dict = {}

    nb_token = int(subprocess.run(['cat %s/%s/*.conllu | egrep "^[0-9]+\t" | wc -l' % (basedir, corpus)], capture_output=True, shell=True, encoding='UTF-8').stdout)
    nb_sent = int(subprocess.run(['cat %s/%s/*.conllu | grep "^# sent_id =" | wc -l' % (basedir, corpus)], capture_output=True, shell=True, encoding='UTF-8').stdout)

    if col == "FEATS":
        command = 'cat %s/%s/*.conllu | egrep "^[0-9]+\t" | cut -f 6 | grep -v "_" | tr "|" "\n" | cut -f 1 -d "=" | sort | uniq -c' % (basedir, corpus)
    elif col == "DEPS":
        command = 'cat %s/%s/*.conllu | egrep "^[0-9]+\t" | cut -f 8 | sort | uniq -c' % (basedir, corpus)
    elif col == "MISC":
        command = 'cat %s/%s/*.conllu | egrep "^[0-9]+\t" | cut -f 10 | grep -v "_" | tr "|" "\n" | grep "=" | cut -f 1 -d "=" | sort | uniq -c' % (
            basedir, corpus)
    else:
        print ("Unknown col spec `%s`, stopped" % col)
    raw = subprocess.run([command], capture_output=True, shell=True, encoding='UTF-8')
    col_cpt = 0 
    for line in raw.stdout.split("\n"):
        fields = line.strip().split(" ")
        if len(fields) == 2:
            occ = int(fields[0])
            col_cpt += 1
            sub_dict[fields[1]] = (occ, occ/nb_sent, occ/nb_token)
    nb_col[corpus] = col_cpt
    dict[corpus] = sub_dict

for corpus in corpus_list:
    if verbose:
        print ("---> %d/%d: %s" % (corpus_cpt + 1, len(corpus_list), corpus))
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

# build the Grew pattern
def pattern_feats (feature):
    # turn UD notation "Number[psor]" into Grew notation "Number__psor"
    sp = re.split("\[|\]", feature)
    grew_feature = sp[0]+"__"+sp[1] if len(sp) > 1 else feature
    return (['pattern { N [%s] }' % grew_feature], "N.%s" % grew_feature)

# build the Grew pattern
def pattern_misc (feature):
    prefix = "__MISC__" if feature in ud_feats_2_10 else ""
    # turn UD notation "Number[psor]" into Grew notation "Number__psor"
    sp = re.split("\[|\]", feature)
    grew_feature = prefix + (sp[0]+"__" + sp[1] if len(sp) > 1 else feature)
    return (['pattern { N [%s] }' % grew_feature], "N.%s" % grew_feature)

def pattern_deps (dep):
    return (['pattern {M -[%s]-> N}' %dep], None)

def pattern (x):
    if col == "FEATS":
        return pattern_feats(x)
    elif col == "DEPS":
        return pattern_deps(x)
    elif col == "MISC":
        return pattern_misc(x)
    else:
        print("Unknown col spec `%s`, stopped" % col)
        exit(2)

def title (x):
    if col == "FEATS":
        return "## Usage of features in UD treebanks ("+version+") in `FEATS` CoNLL column"
    elif col == "DEPS":
        return "## Usage of dependency relations in SUD treebanks ("+version+")"
    elif col == "MISC":
        return "## Usage of features in UD treebanks ("+version+") in `MISC` CoNLL column (see [Grew doc](https://grew.fr/doc/conllu/#how-the-misc-field-is-handled-by-grew))"
    else:
        print("Unknown col spec `%s`, stopped" % col)
        exit(2)

def build_row(corpus):
    d = dict[corpus]
    l = len(d)
    d.update({"treebank": corpus+"@"+version+" ⮕ "+str(l)})
    return d

grid = {
    "title": title(col),
    "grew_match": 
        {feat: {
            "code": pattern(feat)[0], 
            "key": pattern(feat)[1], 
            "users": users}
        for (feat, users) in key_list },
    "columns": [{"field": feat, "headerName": feat+" ⮕ "+str(users)} for (feat, users) in key_list],
    "cells": [build_row(corpus) for corpus in corpus_list]
}

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# ==== Step 5 ====
# Store the final JSON object in a file
with open(out_file, "w") as file:
    json.dump(grid, file, indent=2)
