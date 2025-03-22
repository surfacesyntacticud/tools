SUD=/Users/guillaum/resources/sud-treebanks-v2.15
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
		--timestamp \
		--treebanks ${CORPUSBANK}/parseme_1.2.json \
		--requests parseme/validation_req.json \
		> html/parseme/valid@1.2.json

parseme_13_valid:
	python3 build_table.py TBR \
		--instance https://parseme.grew.fr \
		--title "## Parseme 1.3 validation" \
		--timestamp \
		--treebanks ${CORPUSBANK}/parseme_1.3.json \
		--requests parseme/validation_req.json \
		> html/parseme/valid@1.3.json

parseme_latest_valid:
	python3 build_table.py TBR \
		--instance https://parseme.grew.fr \
		--title "## Parseme latest validation" \
		--timestamp \
		--treebanks ${CORPUSBANK}/parseme_latest.json \
		--requests parseme/validation_req.json \
		> html/parseme/valid@latest.json

parseme_12_labels:
	python3 build_table.py TBC \
		--instance https://parseme.grew.fr \
		--title "## Parseme 1.2 sorted by labels" \
		--timestamp \
		--treebanks ${CORPUSBANK}/parseme_1.2.json \
		--request parseme/label_req.json \
		--clustering_key MWE.label \
		--total \
		> html/parseme/labels@1.2.json

parseme_13_labels:
	python3 build_table.py TBC \
		--instance https://parseme.grew.fr \
		--title "## Parseme 1.3 sorted by labels" \
		--timestamp \
		--treebanks ${CORPUSBANK}/parseme_1.3.json \
		--request parseme/label_req.json \
		--clustering_key MWE.label \
		--total \
		> html/parseme/labels@1.3.json

parseme_latest_labels:
	python3 build_table.py TBC \
		--instance https://parseme.grew.fr \
		--title "## Parseme latest sorted by labels" \
		--timestamp \
		--treebanks ${CORPUSBANK}/parseme_latest.json \
		--request parseme/label_req.json \
		--clustering_key MWE.label \
		--total \
		> html/parseme/labels@latest.json

parseme_12_sizes:
	python3 build_table.py TBC \
		--instance https://parseme.grew.fr \
		--title "## Parseme 1.2 sorted by size (nb of tokens)" \
		--timestamp \
		--treebanks ${CORPUSBANK}/parseme_1.3.json \
		--request parseme/label_req.json \
		--clustering_key MWE.__out__ \
		--total \
		> html/parseme/sizes@1.2.json

parseme_13_sizes:
	python3 build_table.py TBC \
		--instance https://parseme.grew.fr \
		--title "## Parseme 1.3 sorted by size (nb of tokens)" \
		--timestamp \
		--treebanks ${CORPUSBANK}/parseme_1.3.json \
		--request parseme/label_req.json \
		--clustering_key MWE.__out__ \
		--total \
		> html/parseme/sizes@1.3.json

parseme_latest_sizes:
	python3 build_table.py TBC \
		--instance https://parseme.grew.fr \
		--title "## Parseme latest sorted by size (nb of tokens)" \
		--timestamp \
		--treebanks ${CORPUSBANK}/parseme_latest.json \
		--request parseme/label_req.json \
		--clustering_key MWE.__out__ \
		--total \
		> html/parseme/sizes@latest.json

label_upos_French-GSD:
	python3 build_table.py DC \
		--treebank "{\"SUD_French-GSD@2.15\": \"${SUD}/SUD_French-GSD\"}" \
		--title "## edge label and dependant UPOS (SUD_French-GSD@2.15)" \
		--timestamp \
		--request "edge.json" \
		--row_key "e.label" \
		--col_key "N.ExtPos/upos" \
		> html/SUD_French-GSD/label_upos@2.15.json

amb_lemma_French-GSD:
	python3 build_table.py DC \
		--treebank "{\"SUD_French-GSD@2.15\": \"${SUD}/SUD_French-GSD\"}" \
		--title "## ambiguous lemmas UPOS (SUD_French-GSD@2.15)" \
		--timestamp \
		--request "lemma.json" \
		--row_key "N.lemma" \
		--col_key "N.upos" \
		--filter \
		> html/SUD_French-GSD/amb_lemma@2.15.json

pos_features_French-GSD:
	python3 pos_features.py \
		--treebank "{\"SUD_French-GSD@2.15\": \"${SUD}/SUD_French-GSD\"}" \
		> html/SUD_French-GSD/pos_features@2.15.json

subrel:
	python3 build_table.py TBC \
		--instance https://universal.grew.fr \
		--config sud \
		--treebanks ${CORPUSBANK}/sud_latest.json \
		--title "## subrel usage in native SUD" \
		--timestamp \
		--request sud/subrel.json \
		--clustering_key e.2 \
		--total \
		> html/sud/subrel.json

deep:
	python3 build_table.py TBC \
		--instance https://universal.grew.fr \
		--config sud \
		--treebanks ${CORPUSBANK}/sud_latest.json \
		--title "## subrel usage in native SUD" \
		--timestamp \
		--request sud/deep.json \
		--clustering_key e.deep \
		--total \
		> html/sud/deep.json

run_test:
	python3 build_table.py TBR \
		--config sud \
		--instance https://universal.grew.fr \
		--title "## TEST 2 Treebanks / multi-request" \
		--timestamp \
		--treebanks test/two_treebanks.json \
		--requests test/requests.json \
		> html/test/test_TBR.json

gl:
	python3 build_table.py TBR \
		--config sud \
		--instance https://universal.grew.fr \
		--title "## Guidelines table" \
		--timestamp \
		--treebanks /Users/guillaum/github/surfacesyntacticud/guidelines/tools/french/french_table_json/sud_french.json \
		--requests /Users/guillaum/github/surfacesyntacticud/guidelines/tools/french/french_request_json/request_output_french_subj.json \
		# > html/test/test_TBR.json


start_test: stop
	python3 -m http.server --directory html ${PORT} &
	open "http://localhost:${PORT}?data=test/test_TBR"
