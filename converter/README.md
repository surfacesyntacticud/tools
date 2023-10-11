
# The UD/SUD converter tool

This repository contains a set of Graph Rewriting rules which can be used with the [Grew software](http://grew.fr) for conversion from [UD](http://universaldependencies.org/) to [SUD](https://surfacesyntacticud.github.io/) and the other way.

Examples of converted data are available [here](https://surfacesyntacticud.github.io/data).

## HOWTO use the conversion system

You first have to install the Grew software (see [instructions](https://grew.fr/usage/install/) page).

:warning: Since version 1.4, the new argument `-config sud` is needed to have a proper printing of SUD specific edge relations with deep features like `subj@pass`.

### Conversion from UD to SUD

```
grew transform -grs grs/UD_to_SUD.grs -config sud -i input_UD_file.conllu -o output_SUD_file.conllu
```

### Conversion from SUD to UD

```
grew transform -grs grs/SUD_to_UD.grs -config sud -i input_SUD_file.conllu -o output_UD_file.conllu
```


### Autmatic tests
You can run automatic tests defined in `./test2/tests_description.json` to see if the rules are being applied correctly.
You need to add a folder that has the same name of the grs file inside `test2/data/` with both a `source.conllu` and an `expected conllu`.

### test description
Add an entry for your grs rule inside `./test2/tests_description.json` with the following entries :
```json
[
    {
        "TEST_FOLDER_NAME": "zh_mSUD_to_SUD",
        "GRS_FILE": "zh_mSUD_to_SUD.grs",
        "STRAT_NAME": "zh_mSUD_to_SUD_main",
        "CONFIG_TYPE": "sud"
    }
]
```

### Tests command
Using docker, run the following commands

```bash
docker build -t grs_test . 
docker run grs_test
```