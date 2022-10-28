# CoNLL utilities

This folder contains some small tools to fix validation problems in CoNLL UD data.

# Rebuild text metadata

The script `fix_text.ml` rebuild the metadata field `# text = …` from the token of the sentence.

Usage:

```
ocaml str.cma fix_text.ml [input_file] > [output_file]
```

# Unicode normalisation

Usage:

```
python unicode_normalize.py [input_file] > [output_file]
```

