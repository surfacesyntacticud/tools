# Morph-based to word-based conversion

NOTE: Page to te update, GRS moved to `converter/grs/bej_mSUD_to_SUD.grs`.

The GRS file `morph2word.grs` is used to convert a morph-based SUD or UD corpus into a word-based corpus counterpart.

It was built and tested on the [Beja SUD treebank](https://github.com/surfacesyntacticud/SUD_Beja-NSC).

See: Sylvain Kahane, Martine Vanhove, Rayan Ziane and Bruno Guillaume, "[A morph-based and a word-based treebank for Beja](https://aclanthology.org/2021.tlt-1.5.pdf)", SyntaxFest 2021

The system will probably need to be adapted to be applied on other corpora or languages.

Two kinds of affixes are taken into account: inflectional and derivational; annotated with features `TokenType=InflAff` and `TokenType=DerAff`.

## Usage

**Note:** Minimum [Grew](https://grew.fr) version is 1.8.

The commands used for the conversion of Beja:

```
mkdir -p word_based
grew transform -config sud -grs morph2word.grs -i BEJ_MV_NARR_01_shelter.conllu -o word_based/BEJ_MV_NARR_01_shelter.conllu
grew transform -config sud -grs morph2word.grs -i BEJ_MV_NARR_03_camel.conllu -o word_based/BEJ_MV_NARR_03_camel.conllu
```

Try the GRS online on Grew-web:
 * [BEJ_MV_NARR_03_camel](http://transform.grew.fr/?grs=https://raw.githubusercontent.com/surfacesyntacticud/tools/master/morph2word/morph2word.grs&corpus=https://raw.githubusercontent.com/surfacesyntacticud/SUD_Beja-NSC/master/BEJ_MV_NARR_03_camel.conllu)
 * [BEJ_MV_NARR_01_shelter](http://transform.grew.fr/?grs=https://raw.githubusercontent.com/surfacesyntacticud/tools/master/morph2word/morph2word.grs&corpus=https://raw.githubusercontent.com/surfacesyntacticud/SUD_Beja-NSC/master/BEJ_MV_NARR_01_shelter.conllu)
