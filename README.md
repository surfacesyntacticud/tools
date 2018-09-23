# SUD annotation scheme

SUD id a surface-syntactic annotation scheme that is near-isomorphic to the Universal Dependencies (UD) annotation scheme while following distributional criteria for defining the dependency tree structure and
the naming of the syntactic functions.

For more information, consult the related publication:

 * Kim Gerdes, Bruno Guillaume, Sylvain Kahane and Guy Perrier. [SUD or Surface-Syntactic Universal Dependencies: An annotation scheme near-isomorphic to UD](http://universaldependencies.org/udw18/PDFs/33_Paper.pdf) in proceedings of [Universal Dependencies Workshop 2018](http://universaldependencies.org/udw18/).

# Universal dependencies corpora converted in SUD

 * Download the full set of 122 UD corpora (version 2.2) converted in SUD format: [sud-treebanks-v2.2.tgz](http://www.grew.fr/download/sud-treebanks-v2.2.tgz)
 * Acces to separate files download: [here](sud-treebanks-v2.2.md)

# Conversion Rules

The conversion rules are written for the [Grew software](http://grew.fr):

 * from UD to SUD: [`UD_to_SUD.grs`](https://gitlab.inria.fr/grew/SUD/blob/UDW18/grs/UD_to_SUD.grs)
 * from SUD to UD: [`SUD_to_UD.grs`](https://gitlab.inria.fr/grew/SUD/blob/UDW18/grs/SUD_to_UD.grs)

To apply the conversion, you have to install Grew (see [instructions](http://grew.fr/install)) and use one of the follwing commands:

 * `grew transform -grs UD_to_SUD.grs -i <input_UD_file.conllu> -o <output_SUD_file.conllu>`
 * `grew transform -grs SUD_to_UD.grs -i <input_SUD_file.conllu> -o <output_UD_file.conllu>`
