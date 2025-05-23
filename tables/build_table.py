import sys
import subprocess
import json
import re
import glob
import os.path
import argparse
from xml.dom.expatbuilder import parseString


# The list of features used in UD 2.16 is needed or generated the right Grew pattern for the MISC case
# See: https://grew.fr/doc/conllu/#how-the-misc-field-is-handled-by-grew
ud_feats_2_16 = [
    "Abbr", "Accomp", "AdjType", "AdpType", "AdvType", "Advlz", "Agglutination", "Also", "Analyt", "Animacy", "Animacy[gram]", "Animacy[obj]", "Aspect",
    "Assoc", "BadStyle",
    "Case", "Caus", "Cfm", "Clas", "Class",
    "CleftType", "Clitic", "Clusivity", "Clusivity[obj]", "Clusivity[psor]", "Clusivity[subj]", "Compound", "Comt", "Conces",
    "ConjType", "Connegative", "Contrast", "Contv", "Corf", "Decl", "Definite", "Definitizer", "Degree", "Deixis",
    "DeixisRef", "Deixis[psor]", "Delib", "Deo", "Derivation", "Determ", "Detrans", "Dev", "Dialect", "Dist", "Dyn", "Echo", "Emph",
    "Emphatic", "Encl", "Ergative", "Evident", "Excl", "ExtPos", "Fact", "False", "Foc", "Focus", "FocusType", "Foreign", "Form", "Gender",
    "Gender[abs]", "Gender[cs]", "Gender[dat]", "Gender[erg]", "Gender[io]", "Gender[lo]", "Gender[obj]", "Gender[po]", "Gender[psor]", "Gender[refl]", "Gender[ro]", "Gender[subj]",
    "HebBinyan", "HebExistential", "Hnfc", "Htp", "Hum", "Human", "Hyph",
    "Imprs", "Incorp", "InfForm", "InflClass", "InflClass[nominal]", "Int", "Intens", "Intense", "Intension",
    "Irr", "LangId", "Language", "Link", "LongForm", "Modal", "Modality", "Mood", "Morph", "Movement", "Mutation", "NameType", "NCount", "NegationType",
    "Neutral", "Nmzr", "Nominal", "Nomzr", "NonFoc", "NounBase", "NounClass", "NounType", "Number", "Number[abs]", "Number[cs]", "Number[dat]",
    "Number[erg]", "Number[grnd]", "Number[io]", "Number[lo]", "Number[obj]", "Number[po]", "Number[psed]", "Number[psor]", "Number[refl]",
    "Number[ro]", "Number[subj]", "NumForm", "NumType", "NumValue", "Obl", "Orth", "PartForm", "PartType", "PartTypeQpm", "Pcl", "Person",
    "Person[abs]", "Person[cs]", "Person[dat]", "Person[erg]", "Person[grnd]", "Person[io]", "Person[lo]", "Person[obj]", "Person[po]", "Person[psor]",
    "Person[refl]", "Person[ro]", "Person[subj]", "Polarity", "Polite", "Polite[abs]", "Polite[dat]", "Polite[erg]", "Position", "Poss", "Possessed", "Pred",
    "Prefix", "PrepCase", "PrepForm", "Priv", "PronClass", "PronType", "Proper", "Prp", "PunctSide", "PunctType", "Purp", "RcpType", "Recip", "Red", "Redup",
    "Reflex", "Reflex[obj]", "Reflex[subj]", "Rel", "Reln", "RelType", "Report", "Speech", "Strength", "Style", "Subcat", "SubForm", "SubGender", "Subord",
    "Subordinative", "Tense", "Top", "Trans", "Tv", "Typo", "Uninflect", "Valency", "Variant", "Ventive", "VerbClass", "VerbForm", "VerbStem", "VerbType", "Voice",
    "Shared"
  ]



parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("basedir", help = "The main folder where all corpora are stored as subdirs")
parser.add_argument("columns", help = "Must be one either of the values 'DEPS', 'UDEPS', 'DEEP', 'SUBREL:xxx (where xxx is a udep), 'META', 'FEATS', 'MISC', 'FEAT:xxx' (where xxx is a feature name)")
parser.add_argument("-f", "--filter", help = "The template for selecting treebanks", default="*")
parser.add_argument("-o", "--out_file", help = "The name of the output json file")
parser.add_argument("-p", "--prefix", default="", help = "The prefix used in Grew-match naming of the corpus")
parser.add_argument("-i", "--instance", default="universal", help = "Grew-match instance")
parser.add_argument("-s", "--suffix", default="@2.16", help = "The suffix used in Grew-match naming of the corpus")
parser.add_argument("-c", "--collection", help = "The name of the collection of corpora")
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

    nb_token = int(subprocess.run(['cat %s/%s/*.conllu | egrep "^[0-9]+\t" | wc -l' % (args.basedir, corpus)], capture_output=True, shell=True, encoding='UTF-8').stdout)
    nb_sent = int(subprocess.run(['cat %s/%s/*.conllu | grep "^# sent_id =" | wc -l' % (args.basedir, corpus)], capture_output=True, shell=True, encoding='UTF-8').stdout)

    if args.columns == "DEPS":
        command = 'cat %s/%s/*.conllu | egrep "^[0-9]+\t" | cut -f 8 | sort | uniq -c' % (args.basedir, corpus)
    elif args.columns == "UDEPS":
        command = 'cat %s/%s/*.conllu | egrep "^[0-9]+\t" | cut -f 8 | cut -f 1 -d ":" | cut -f 1 -d "@" | cut -f 1 -d "$" | sort | uniq -c' % (args.basedir, corpus)
    elif args.columns == "DEEP":
        command = 'cat %s/%s/*.conllu | egrep "^[0-9]+\t" | cut -f 8 | grep "@" | cut -f 2 -d "@" | sort | uniq -c' % (args.basedir, corpus)
    elif args.columns[0:7] == "SUBREL:":
        dep = args.columns[7:]
        dep = dep if dep != "_aux" else "aux"
        command = 'cat %s/%s/*.conllu | egrep "^[0-9]+\t" | cut -f 8 | cut -f 1 -d "@" | cut -f 1 -d "$" | egrep "^%s(:|$)" | sort | uniq -c' % (args.basedir, corpus, dep)
    elif args.columns == "META":
        command = 'cat %s/%s/*.conllu | grep "^# " | grep " = " | cut -f 1 -d "=" | sed "s/# *//" | sed "s/ $//" | grep -v "^text$" | grep -v "^sent_id$" | grep -v "^global.columns$" | sort | uniq -c' % (args.basedir, corpus)
    elif args.columns == "FEATS":
        command = 'cat %s/%s/*.conllu | egrep "^[0-9]+\t" | cut -f 6 | grep -v "_" | tr "|" "\n" | cut -f 1 -d "=" | sort | uniq -c' % (args.basedir, corpus)
    elif args.columns == "MISC":
        command = 'cat %s/%s/*.conllu | egrep "^[0-9]+\t" | cut -f 10 | tr "|" "\n" | grep "=" | cut -f 1 -d "=" | sort | uniq -c' % (args.basedir, corpus)
    elif args.columns[0:5] == "FEAT:":
        feat = args.columns[5:]
        command = 'cat %s/%s/*.conllu | egrep "^[0-9]+\t" | cut -f 6 | tr "|" "\n" | grep "^%s=" | cut -f 2 -d "=" | sort | uniq -c' % (args.basedir, corpus, feat)
    else:
        raise Exception('Unknonwn column definition', args.columns)
    raw = subprocess.run([command], capture_output=True, shell=True, encoding='UTF-8')
    column_cpt = 0
    for line in raw.stdout.split("\n"):
        fields = line.strip().split(" ")
        if len(fields) >= 2:
            occ = int(fields[0])
            value = " ".join(fields[1:])
            column_cpt += 1
            sub_dict[value] = (occ, occ/nb_sent, occ/nb_token)
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
def pattern (x):
    if args.columns == "DEPS":
        return (['pattern {M -[%s]-> N}' % x], None)
    elif args.columns[0:7] == "SUBREL:":
        rel = x.split(":")
        if len(rel) == 1:
            return (['pattern {M -[1=%s,!2]-> N}' % x], None)
        else:
            return (['pattern {M -[1=%s,2=%s]-> N}' % (rel[0],rel[1])], None)
    elif args.columns == "UDEPS":
        return (['pattern {M -[1=%s]-> N}' % x], None)
    elif args.columns == "DEEP":
        return (['pattern {M -[deep=%s]-> N}' % x], None)
    elif args.columns == "META":
        ident = re.fullmatch ("[A-Za-z_-]+", x)
        if (ident is not None):
            return (['global { %s = * }' % x], None)
        else:
            return ["__NO_GREW_SYNTAX__", None]
    elif args.columns == "FEATS":
        grew_feature = grew_feat_name(x)
        return (['pattern { N [%s] }' % grew_feature], "N.%s" % grew_feature)
    elif args.columns == "MISC":
        prefix = "__MISC__" if x in ud_feats_2_16 else ""
        grew_feature = prefix + grew_feat_name(x)
        return (['pattern { N [%s] }' % grew_feature], "N.%s" % grew_feature)
    elif args.columns[0:5] == "FEAT:":
        feat = args.columns[5:]
        return (['pattern { N [%s="%s"] }' % (grew_feat_name(feat), x)], None)
    else:
        raise Exception('Unknonwn column definition', args.columns)

def title (x):
    if args.columns == "DEPS":
        return "## Usage of dependency relations (with subtypes)"
    elif args.columns == "UDEPS":
        return "## Usage of dependency relations (without subtypes)"
    elif args.columns == "DEEP":
        return "## Usage of deep extension"
    elif args.columns[0:7] == "SUBREL:":
        dep = args.columns[7:]
        dep = dep if dep != "_aux" else "aux"
        return "## Usage of subtypes of relation `%s`" % dep
    elif args.columns == "META":
        return "## Usage of meta data (≠ text and sent_id)"
    elif args.columns == "FEATS":
        return "## Usage of features in `FEATS` CoNLL column"
    elif args.columns == "MISC":
        return "## Usage of features in `MISC` CoNLL column (see [Grew doc](https://grew.fr/doc/conllu/#how-the-misc-field-is-handled-by-grew))"
    elif args.columns[0:5] == "FEAT:":
        feat = args.columns[5:]
        return "## Usage of `%s` feature" % feat
    else:
        raise Exception('Unknonwn column definition', args.columns)

def build_row(corpus):
    d = dict[corpus]
    d.update({"treebank": args.prefix+corpus+args.suffix})
    return d

grid = {
    "title": title(args.columns) + (" ••• " + args.collection) if args.collection != None else "",
    "instance": args.instance,
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
