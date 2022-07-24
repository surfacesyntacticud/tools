UD=/users/guillaum/resources/ud-treebanks-v2.10
SUD=/users/guillaum/resources/sud-treebanks-v2.10

sud:
	mkdir -p sud
	python build_table.py -f "*UD_B*" -o sud/sud_deps.json ${SUD} DEPS

ud:
	mkdir -p ud
	python build_table.py -f "*UD_B*" -o ud/ud_deps.json ${UD} DEPS
	python build_table.py -f "*UD_B*" -o ud/ud_feats.json ${UD} FEATS
	python build_table.py -f "*UD_B*" -o ud/ud_misc.json ${UD} MISC

ud_feats:
	mkdir -p ud
	@for feat in PronType Gender VerbForm NumType Animacy Mood Poss NounClass Tense Reflex Number Aspect Foreign Case Voice Abbr Definite Evident Typo Degree Polarity Person Polite Clusivity ; do \
		echo "================= Building table for feature: $$feat =================" ; \
		python build_table.py -f "*UD_B*" -o ud/$$feat.json ${UD} $$feat ; \
	done

