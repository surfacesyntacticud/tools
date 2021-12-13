# Morph-based to word-based conversion

The GRS file `morph2word.grs` is used to convert a morph-based SUD or UD corpus into a word-based corpus counterpart.

It was built and tested on the [Beja SUD treebank](https://github.com/surfacesyntacticud/SUD_Beja-NSC).

See: Sylvain Kahane, Martine Vanhove, Rayan Ziane and Bruno Guillaume, "A morph-based and a word-based treebank for Beja", SyntaxFest 2021

**TODO**: add link to the paper when available online

The system will probably need to be adapted to be applied on some other corpora.

Two kinds of affixes are taken into account: inflectional and derivational; annotated with features TokenType=InflAff and TokenType=DerAff.

**Note:** Minimum Grew version is 1.8 (not released yet).

Try the GRS online on Grew-web:
 * [BEJ_MV_NARR_03_camel](http://transform.grew.fr/?grs=https://raw.githubusercontent.com/surfacesyntacticud/tools/master/morph2word/morph2word.grs&corpus=https://raw.githubusercontent.com/surfacesyntacticud/SUD_Beja-NSC/master/BEJ_MV_NARR_03_camel.conllu)
 * [BEJ_MV_NARR_01_shelter](http://transform.grew.fr/?grs=https://raw.githubusercontent.com/surfacesyntacticud/tools/master/morph2word/morph2word.grs&corpus=https://raw.githubusercontent.com/surfacesyntacticud/SUD_Beja-NSC/master/BEJ_MV_NARR_01_shelter.conllu)