## Prediction of the `wordform` feature
The Python script `wordform_prediction.py` can be used to predict a part of the `wordform` features needed in annotated data to express the `textform`/`wordform` presentation of the link between input text and word forms (following the proposition in [#683](https://github.com/UniversalDependencies/docs/issues/683); see also [Grew-match doc](http://grew.fr/match_doc/#additional-features-textform-and-wordform)).

### Script usage

The script is run with the command:
`./wordform_prediction.py <infile> <outfile>`.

### Description
For each token line, if:

 * it is not a proper noun: `UPOS` ≠ `PROPN`
 * and it is not a lowercase word: `FORM` ≠ `lowercase(FORM)`

then a new feature is added in column 10 (`MISC`) with feature name `wordform` and with value `lowercase(FORM)`.

### Example

Input:

```
# sent_id = fr-ud-train_11907
# text = Résultats Officiels FIS
1	Résultats	résultat	NOUN	_	Gender=Masc|Number=Plur	0	root	_	_
2	Officiels	officiel	ADJ	_	Gender=Masc|Number=Plur	1	mod	_	_
3	FIS	FIS	PROPN	_	_	1	appos	_	_
```

Output:

```
# sent_id = fr-ud-train_11907
# text = Résultats Officiels FIS
1	Résultats	résultat	NOUN	_	Gender=Masc|Number=Plur	0	root	_	wordform=résultats
2	Officiels	officiel	ADJ	_	Gender=Masc|Number=Plur	1	mod	_	wordform=officiels
3	FIS	FIS	PROPN	_	_	1	appos	_	_
```

### Warning
In practice, the output should be manually validated or corrected. A few examples in French:

 * the form *A* may correspond to the wordform *à* in *A la plage* and to wordform *a* in *a-t-il décidé ?*
 * the capital *E* can be lowercased as *e*, *é* or *è*

