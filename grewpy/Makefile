SUD=/Users/guillaum/resources/sud-treebanks-v2.12
PORT=8998
PID=`lsof -t -i :${PORT}`
GREW_MATCH_CONFIG=/Users/guillaum/gitlab/grew/grew_match_config

self_doc:
	@echo " - make start ==> start a local webserver"
	@echo " - make stop ==> stop the local webserver"
	@echo " - make web ==> rebuild list.html file from list.md"
	@echo " - make all: build all target below"
	@echo "   - make stat_pos_features"
	@echo "   - make label_upos"
	@echo "   - make amb_lemma"
	@echo "   - make adj_lemma_pos"
	@echo "   - make parseme"
	@echo " - make clean"

start:
	python3 -m http.server --directory html ${PORT} &
	open "http://localhost:${PORT}"

stop:
	@if [ -z "$(PID)" ]; then \
		echo "No process running on PORT ${PORT}"; \
	else \
		kill -9 ${PID}; \
		echo "Process killed"; \
	fi

web:
	pandoc --standalone --template html/template.html html/list.md -o html/list.html

parseme_12_valid:
	python3 build_table.py TBR \
		--instance https://parseme.grew.fr \
		--title "## Parseme 1.2 validation" \
		--treebanks ${GREW_MATCH_CONFIG}/corpora/parseme_1.2.json \
		--requests parseme/validation_req.json \
		> html/parseme/valid@1.2.json

parseme_13_valid:
	python3 build_table.py TBR \
		--instance https://parseme.grew.fr \
		--title "## Parseme 1.3 validation" \
		--treebanks ${GREW_MATCH_CONFIG}/corpora/parseme_1.3.json \
		--requests parseme/validation_req.json \
		> html/parseme/valid@1.3.json

parseme_12_labels:
	python3 build_table.py TBC \
		--instance https://parseme.grew.fr \
		--title "## Parseme 1.2 sorted by labels" \
		--treebanks ${GREW_MATCH_CONFIG}/corpora/parseme_1.2.json \
		--request parseme/label_req.json \
		--clustering_key MWE.label \
		--total \
		> html/parseme/labels@1.2.json

parseme_13_labels:
	python3 build_table.py TBC \
		--instance https://parseme.grew.fr \
		--title "## Parseme 1.3 sorted by labels" \
		--treebanks ${GREW_MATCH_CONFIG}/corpora/parseme_1.3.json \
		--request parseme/label_req.json \
		--clustering_key MWE.label \
		--total \
		> html/parseme/labels@1.3.json



label_upos_French-GSD:
	python3 build_table.py DC \
		--treebank "{\"SUD_French-GSD@2.12\": \"${SUD}/SUD_French-GSD\"}" \
		--title "## edge label and dependant UPOS (SUD_French-GSD@2.12)" \
		--request "edge.req" \
		--row_key "e.label" \
		--col_key "N.ExtPos/upos" \
		> html/SUD_French-GSD/label_upos@2.12.json

amb_lemma_French-GSD:
	python3 build_table.py DC \
		--treebank "{\"SUD_French-GSD@2.12\": \"${SUD}/SUD_French-GSD\"}" \
		--title "## ambiguous lemmas UPOS (SUD_French-GSD@2.12)" \
		--request "lemma.req" \
		--row_key "N.lemma" \
		--col_key "N.upos" \
		--filter \
		> html/SUD_French-GSD/amb_lemma@2.12.json

pos_features_French-GSD:
	python3 pos_features.py \
		--treebank "{\"SUD_French-GSD@2.12\": \"${SUD}/SUD_French-GSD\"}" \
		> html/SUD_French-GSD/pos_features@2.12.json
