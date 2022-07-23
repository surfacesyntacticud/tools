# Universal tables: Web-based tables showing stats about (S)UD usage of features and relations

This folder contains the website files, a few tables and the python code for the table constructions.
The rendering of the table is done with [ag-grid JS library](https://www.ag-grid.com/).

## Main features
 * Filtering is available on `Rows` (*i.e.* on Treebanks names) or on `Columns` (*i.e.* either feature name or dependency relation).
    * filtering on rows automatically filters the non empty columns
    * filtering on columns automatically filters the non empty rows   
 * Columns are sortable and can be moved
 * Counting is available as: 
    * `Occurences` &rarr; the number of times the corresponding element is present in the corpus
    * `Ratio / sents` &rarr; the `Occurences` number divided by the number of sentences in the corpus
    * `Ratio / tokens` &rarr; the `Occurences` number divided by the number of tokens in the corpus
 * Each observation is linked to a corresponding [Grew-match](http://match.grew.fr) request

## Available tables

* On features usage
  * MISC: http://tables.grew.fr/?data=data/ud_misc
  * FEATS: http://tables.grew.fr/?data=data/ud_feats
* On dependency relations usage
  * UD: http://tables.grew.fr/?data=data/ud_deps
  * SUD: http://tables.grew.fr/?data=data/sud_deps

## Local usage

In the `tables` folder, run the command `python -m http.server`.
Then used one of the links: [MISC](http://localhost:8000?data=data/ud_misc), [FEATS](http://localhost:8000?data=data/ud_feats), [UD relations](http://localhost:8000?data=data/ud_deps) or [SUD relations](http://localhost:8000?data=data/sud_deps).

## Python script

The python script `build_table.py` builds the JSON file.

## Issues
Problems, suggestions… can be reported [here](https://github.com/surfacesyntacticud/tools/issues/new?labels=tables).

## TODO
 * Add args parsing in Python script (Parameters are hard-coded :-1:)
 * Add a table per feature, showing features values used in different treebanks

 ## Acknowledgement

 Thanks to Santiago for letting me know about the [ag-grid JS library](https://www.ag-grid.com/)! 
 Thanks to the users of the previous versions for their feedback and suggestions.
