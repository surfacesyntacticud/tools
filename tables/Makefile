UD=/users/guillaum/resources/ud-treebanks-v2.10
SUD=/users/guillaum/resources/sud-treebanks-v2.10

sud_build:
	mkdir -p sud
	python build_table.py -f "*UD_*" -o sud/deps.json ${SUD} DEPS

ud_build:
	mkdir -p ud
	python build_table.py -f "*UD_*" -o ud/deps.json ${UD} DEPS
	python build_table.py -f "*UD_*" -o ud/feats.json ${UD} FEATS
	python build_table.py -f "*UD_*" -o ud/misc.json ${UD} MISC

ud_feats:
	mkdir -p ud
	@for feat in PronType Gender VerbForm NumType Animacy Mood Poss NounClass Tense Reflex Number Aspect Foreign Case Voice Abbr Definite Evident Typo Degree Polarity Person Polite Clusivity ; do \
		echo "================= Building table for feature: $$feat =================" ; \
		python build_table.py -f "*UD_*" -o ud/$$feat.json ${UD} $$feat ; \
	done

start:
	python -m http.server &
	open "http://localhost:8000?data=data/ud_misc"

stop:
	kill `lsof -t -i :8000`