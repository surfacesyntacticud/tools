
# The UD/SUD converter tool

This repository contains a set of Graph Rewriting rules which can be used with the [Grew software](http://grew.fr) for conversion from [UD](http://universaldependencies.org/) to [SUD](https://surfacesyntacticud.github.io/) and the other way.

Examples of converted data are available [here](https://surfacesyntacticud.github.io/data).

## HOWTO use the conversion system

You first have to install the Grew software (see [instructions](https://grew.fr/usage/install/) page).

### Conversion from UD to SUD

```
grew transform -grs grs/UD_to_SUD.grs -i input_UD_file.conllu -o output_SUD_file.conllu
```

### Conversion from SUD to UD

```
grew transform -grs grs/SUD_to_UD.grs -i input_SUD_file.conllu -o output_UD_file.conllu
```
