# Automatic production of alternative treebanks

This folder contains a few GRS (Graph Rewriting System) to be used with [Grew](https://grew.fr).
These GRS ares used to make automatic conversion of some Treabanks available in the `SUD Auto` menu in http://universal.grew.fr.
These autoamtic converted treebanks are named: *original_treebank_name* + *grs_name*

The GRS are:
 * `fix_typo.grs`: use all `Correct*` feature to recover the "corrected" sentence where `Typo` are identified
   * [SUD_French-GSD+fix_typo](http://universal.grew.fr/?corpus=SUD_French-GSD%2Bfix_typo)
 * `rm_mwt.grs`: ⚠️ developped for French: replace all MWT (multi-word tokens) by regular tokens (in order to be more adapted for parsing)
   * [SUD_French-GSD+rm_mwt](http://universal.grew.fr/?corpus=SUD_French-GSD%2Brm_mwt)
 * `say_dev.grs`: fake GRS to be used as placeholder for real usage of conversion on Zaar data
   * [SUD_Zaar-Autogramm+say_dev](http://universal.grew.fr/?corpus=SUD_Zaar-Autogramm%2Bsay_dev)
 * `gsd2spoken.grs`: update of `SUD_French-GRD` to a spoken setting (to make it more consistent with `SUD_French-Rhapsodie` and `SUD_French-ParisStories`). This system was initially by [@mmahamdi](https://github.com/mmahamdi) (see [here](https://github.com/mmahamdi/SUD_Spoken/blob/20984009b13a267268b0807dcf7ebe3f4abb3b9e/grew_grammars/gsd2spoken.grs) for original version).
   * [SUD_French-GSD+gsd2spoken](http://universal.grew.fr/?corpus=SUD_French-GSD%2Bgsd2spoken)
