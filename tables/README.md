# Code to build the stat tables about UD usage of features and relations

* MISC usages: http://universal.grew.fr/ud_stat/?data=MISC
* FEATS usages: http://universal.grew.fr/ud_stat/?data=FEATS
* DEPS usages: http://universal.grew.fr/ud_stat/?data=DEPS

The python script `ud_stat.py` builds the JSON file with the needed data and the `index.html` displays it, usign the [grid.js](https://gridjs.io/) javascript library.

See `Makefile` for the commands to run the Python script.
