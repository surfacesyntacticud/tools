# Universal tables: Web-based tables showing stats about (S)UD usage of features and relations

This folder contains the website files, a few tables and the python code for the tables construction.
The rendering of the tables is done with [ag-grid JS library](https://www.ag-grid.com/).

## Available tables

The tables are available through the URL https://tables.grew.fr with direct links to the six collections of tables:

 - In SUD:
   - [`https://tables.grew.fr?data=sud_deps/DEPS`](https://tables.grew.fr?data=sud_deps/DEPS): dependency labels usage in the SUD treebanks
   - [`https://tables.grew.fr?data=sud_feats/FEATS`](https://tables.grew.fr?data=sud_feats/FEATS): features usage in SUD treebanks
   - [`https://tables.grew.fr?data=sud_meta/META`](https://tables.grew.fr?data=sud_meta/META): sentences metadata in SUD treebanks

 - in UD:
   - [`https://tables.grew.fr?data=ud_feats/FEATS`](https://tables.grew.fr?data=ud_feats/FEATS): dependency labels usage in the UD treebanks
   - [`https://tables.grew.fr?data=ud_deps/DEPS`](https://tables.grew.fr?data=ud_deps/DEPS): features usage in UD treebanks
   - [`https://tables.grew.fr?data=meta/META`](https://tables.grew.fr?data=meta/META): sentences metadata in UD treebanks

## Web interface 
 - Filtering is available on `Rows` (*i.e.* on Treebanks names) or on `Columns` (*i.e.* dependency relation, feature name or feature value).
    - filtering on rows automatically filters the non empty columns
    - filtering on columns automatically filters the non empty rows
 - Columns are sortable and can be moved
 - Counting in cells is available as:
    - `Occurences` &rarr; the number of times the corresponding element is present in the corpus
    - `Ratio / tokens` &rarr; the `Occurences` number divided by the number of tokens in the corpus
    - `Ratio / sents` &rarr; the `Occurences` number divided by the number of sentences in the corpus
 - Each observation is linked to the corresponding [Grew-match](http://match.grew.fr) request (with a clustering on values in the case of *feature name* tables).

## Issues
Problems, suggestions… can be reported [here](https://github.com/surfacesyntacticud/tools/issues/new?labels=tables).

## Dev info

### Computing tables

The python script `build_table.py` builds the JSON file.
See `python build_table.py --help` or examples in [`Makefile`](./Makefile) for usage. 

### Local rendering of the tables

In the `tables` folder, run the command `python -m http.server`.
Then open of the page http://localhost:8000 to have a local access to the different tables.

## Acknowledgement

 * Thanks to Santiago for letting me know about the perfect [ag-grid JS library](https://www.ag-grid.com/)! 
 * Thanks to the users of the first version for their feedbacks and suggestions.
