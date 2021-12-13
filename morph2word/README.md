# Morph-based to word-based conversion

This GRS file `morph2word.grs` is used to convert a morph-based SUD or UD corpus into a word-based corpus counterpart.

It was built and tested on the [Beja SUD treebank](https://github.com/surfacesyntacticud/SUD_Beja-NSC).
See: Sylvain Kahane, Martine Vanhove, Rayan Ziane and Bruno Guillaume "A morph-based and a word-based treebank for Beja", SyntaxFest 2021
TODO: add link to the paper when available online

The system will probably need adaptation to be applied on some other corpora.

Two kinds of affixes are taken into account: inflectional and derivational; annotated with features TokenType=InflAff and TokenType=DerAff.

**Note:** Minimum Grew version is 1.8 (not released yet).