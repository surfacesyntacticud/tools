
# The converter tool

This tools consists in a set of Graph Rewriting rules which can be used with the [Grew software](http://grew.fr).

Examples of converted data are available [here](https://surfacesyntacticud.github.io/data).

## HOWTO use the conversion system

You first have to install the Grew software (see [instructions](http://grew.fr/install) page).

### Conversion from UD to SUD

```
grew transform -grs UD+_to_SUD.grs -i <input_UD_file.conllu> -o <output_SUD_file.conllu>
```

### Conversion from SUD to UD

```
grew transform -grs SUD_to_UD+.grs -i <input_SUD_file.conllu> -o <output_UD_file.conllu>
```
