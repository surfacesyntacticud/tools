# Universal tables: Web-based tables showing stats about (S)UD usage of features and relations

This folder contains the website files, a few tables and the python code for the table constructions.
The rendering of the tables is done with [ag-grid JS library](https://www.ag-grid.com/).

## Available tables

The tables are available through the URL http://tables.grew.fr with direct links to the tables below:

* On dependency relations
  * In UD 2.10: http://tables.grew.fr/?data=ud/deps
  * In SUD 2.10: http://tables.grew.fr/?data=sud/deps
* On features usage (only given on UD, on SUD the tables would gives the same observations as SUD does not differ from UD at the feature level)
  * In the `FEATS` column in UD 2.10: http://tables.grew.fr/?data=ud/feats
  * In the `MISC` column in UD 2.10: http://tables.grew.fr/?data=ud/misc
* On feature values (only on UD for the same reason), for the features:
  * [PronType](http://tables.grew.fr/?data=ud/PronType)
  * [Gender](http://tables.grew.fr/?data=ud/Gender)
  * [VerbForm](http://tables.grew.fr/?data=ud/VerbForm)
  * [NumType](http://tables.grew.fr/?data=ud/NumType)
  * [Animacy](http://tables.grew.fr/?data=ud/Animacy)
  * [Mood](http://tables.grew.fr/?data=ud/Mood)
  * [Poss](http://tables.grew.fr/?data=ud/Poss)
  * [NounClass](http://tables.grew.fr/?data=ud/NounClass)
  * [Tense](http://tables.grew.fr/?data=ud/Tense)
  * [Reflex](http://tables.grew.fr/?data=ud/Reflex)
  * [Number](http://tables.grew.fr/?data=ud/Number)
  * [Aspect](http://tables.grew.fr/?data=ud/Aspect)
  * [Foreign](http://tables.grew.fr/?data=ud/Foreign)
  * [Case](http://tables.grew.fr/?data=ud/Case)
  * [Voice](http://tables.grew.fr/?data=ud/Voice)
  * [Abbr](http://tables.grew.fr/?data=ud/Abbr)
  * [Definite](http://tables.grew.fr/?data=ud/Definite)
  * [Evident](http://tables.grew.fr/?data=ud/Evident)
  * [Typo](http://tables.grew.fr/?data=ud/Typo)
  * [Degree](http://tables.grew.fr/?data=ud/Degree)
  * [Polarity](http://tables.grew.fr/?data=ud/Polarity)
  * [Person](http://tables.grew.fr/?data=ud/Person)
  * [Polite](http://tables.grew.fr/?data=ud/Polite)
  * [Clusivity](http://tables.grew.fr/?data=ud/Clusivity)

## Main features
 * Filtering is available on `Rows` (*i.e.* on Treebanks names) or on `Columns` (*i.e.* dependency relation, feature name or feature value).
    * filtering on rows automatically filters the non empty columns
    * filtering on columns automatically filters the non empty rows   
 * Columns are sortable and can be moved
 * Counting in cells is available as:
    * `Occurences` &rarr; the number of times the corresponding element is present in the corpus
    * `Ratio / sents` &rarr; the `Occurences` number divided by the number of sentences in the corpus
    * `Ratio / tokens` &rarr; the `Occurences` number divided by the number of tokens in the corpus
 * Each observation is linked to the corresponding [Grew-match](http://match.grew.fr) request (with a clustering on values in the case of *feature name* tables).

## Issues
Problems, suggestions… can be reported [here](https://github.com/surfacesyntacticud/tools/issues/new?labels=tables).

## Dev info

### Computing tables

The python script `build_table.py` builds the JSON file.
See `python build_table.py --help` or examples in [`Makefile`](./Makefile) for usage. 

### Local rendering of the tables

In the `tables` folder, run the command `python -m http.server`.
Then open of the page http://localhost:8000 to have access to the different tables.

## Acknowledgement

 * Thanks to Santiago for letting me know about the perfect [ag-grid JS library](https://www.ag-grid.com/)! 
 * Thanks to the users of the first version for their feedbacks and suggestions.
