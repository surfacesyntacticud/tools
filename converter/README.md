
# The UD/SUD converter tool

This repository contains a set of Graph Rewriting rules which can be used with the [Grew software](http://grew.fr) for conversion from [UD](http://universaldependencies.org/) to [SUD](https://surfacesyntacticud.github.io/) and the other way.

Examples of converted data are available [here](https://surfacesyntacticud.github.io/data).

## HOWTO use the conversion system

You first have to install the most recent version of the Grew software (see [instructions](https://grew.fr/usage/install/) page).

### Universal conversion from UD to SUD

```
grew transform -grs grs/UD_to_SUD.grs -config sud -i input_UD_file.conllu -o output_SUD_file.conllu
```

### Universal conversion from SUD to UD

```
grew transform -grs grs/SUD_to_UD.grs -config sud -i input_SUD_file.conllu -o output_UD_file.conllu
```

### Language specific conversions
For some langauges, there are dedicated conversion systems.
Corresponding files are prefixed by the language code, for instance, `zh_SUD_to_UD.grs` is a conversion from SUD to UD adapted to Chinese annotations; the strategy to used is names like the file with suffix `_main`(`zh_SUD_to_UD_main` in the previous example).
Consult the `grs` folder to see which languages have specific conversions systems.

### Conversion from mSUD to SUD

For Chinese and Beja, additional conversions for mSUD format are available.

Try the Beja GRS online on Grew-web:
 * [BEJ_MV_NARR_03_camel](http://transform.grew.fr/?grs=https://raw.githubusercontent.com/surfacesyntacticud/tools/master/morph2word/morph2word.grs&corpus=https://raw.githubusercontent.com/surfacesyntacticud/SUD_Beja-NSC/master/BEJ_MV_NARR_03_camel.conllu)
 * [BEJ_MV_NARR_01_shelter](http://transform.grew.fr/?grs=https://raw.githubusercontent.com/surfacesyntacticud/tools/master/morph2word/morph2word.grs&corpus=https://raw.githubusercontent.com/surfacesyntacticud/SUD_Beja-NSC/master/BEJ_MV_NARR_01_shelter.conllu)


## Automatic tests
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