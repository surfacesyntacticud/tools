CoNLL utilities

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

# Filter some sent_id

Python script used to filter a corpus based on a `sent_id` list
used to produced train/dev/test split needed in UD release for Sequoia for instance.
Three arguments are needed:
 - arg 1: a file which contains the sent_id list (on sent_id by line)
 - arg 2: the input corpus
 - arg 3: the file where the output is stored



