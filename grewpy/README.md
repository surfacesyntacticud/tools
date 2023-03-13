# Some Python scripts on SUD data

This folder gather some scripts (currently only one!) using the [`grewpy`](https://grew.fr/usage/python) Python lib.

We suppose that `grewpy` version 0.2.0 and `grewpy_backend` version 0.2.0 are installed ([Install doc](https://grew.fr/usage/python)).

## `stat_pos_features.py`

This [script](./stat_pos_features.py) produces a table showing for each UPOS and for each feature name, the ratio of tokens with this UPOS who have the given feature name. 

With `$GSD` set on a folder containing **SUD_French-GSD** data, this [table](stat_pos_features/SUD_French-GSD.md) is produced by the command:

```
python3 stat_pos_features.py $GSD/*.conllu > stat_pos_features/UD_French-GSD.md
```

With data updated on 2023/03/01, the following tables are available:
 - [SUD_Beja-NSC.md](stat_pos_features/SUD_Beja-NSC.md)
 - [SUD_French-GSD.md](stat_pos_features/SUD_French-GSD.md)
 - [SUD_French-ParisStories.md](stat_pos_features/SUD_French-ParisStories.md)
 - [SUD_French-Rhapsodie-GSD.md](stat_pos_features/SUD_French-Rhapsodie-GSD.md)
 - [SUD_Naija-NSC.md](stat_pos_features/SUD_Naija-NSC.md)
 - [SUD_Zaar-Autogramm.md](stat_pos_features/SUD_Zaar-Autogramm.md)
