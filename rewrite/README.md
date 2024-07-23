# Collection of GRS (Graph Rewriting System) to be used with Grew

This folder contains a few GRS (Graph Rewriting System) to be used with [Grew](https://grew.fr).

## Automatic production of alternative treebanks

These GRS are used to make automatic conversions of some treebanks.
The converted treebanks are are named: *original_treebank_name*@*grs_name* and they are available in the `SUD Auto` menu in https://universal.grew.fr.

The available GRS (and associated converted treebanks) are:
 - [`fix_typo.grs`](fix_typo.grs): use all `Correct*` feature to recover the "corrected" sentence where `Typo` are identified
   - [SUD_French-GSD@fix_typo](http://universal.grew.fr/?corpus=SUD_French-GSD@fix_typo)
 - [`rm_mwt.grs`](rm_mwt.grs): ⚠️ developped for French: replace all MWT (multi-word tokens) by regular tokens (in order to be more adapted for parsing)
   - [SUD_French-GSD@rm_mwt](http://universal.grew.fr/?corpus=SUD_French-GSD@rm_mwt)
   - [SUD_French-ParisStories@rm_mwt](http://universal.grew.fr/?corpus=SUD_French-ParisStories@rm_mwt)
   - [SUD_French-Rhapsodie@rm_mwt](http://universal.grew.fr/?corpus=SUD_French-Rhapsodie@rm_mwt)

## Other GRS
Some of these GRS were used during the maintenance of treebanks (mostly in SUD).
There are listed here as example of GRS that can be adated for similar operations on other treebanks.

 - [`gsd2spoken.grs`](gsd2spoken.grs): update of `SUD_French-GSD` to a spoken setting (to make it more consistent with `SUD_French-Rhapsodie` and `SUD_French-ParisStories`). This system was initially written by [@mmahamdi](https://github.com/mmahamdi) (see [here](https://github.com/mmahamdi/SUD_Spoken/blob/20984009b13a267268b0807dcf7ebe3f4abb3b9e/grew_grammars/gsd2spoken.grs) for original version).


