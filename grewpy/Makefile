SUD=/Users/guillaum/github/surfacesyntacticud
PORT=8998
PID=`lsof -t -i :${PORT}`

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
	@make -C html

parseme_valid:
	python3 build_table.py TBR \
		--instance https://parseme.grew.fr \
		--title "## Parseme 1.3 validation" \
		--treebanks parseme/corpora@1.3.json \
		--requests parseme/validation_req.json \
		> html/tables/parseme/valid@1.3.json

parseme_label:
	python3 build_table.py TBC \
		--instance https://parseme.grew.fr \
		--title "## Parseme 1.3 sorted by labels" \
		--treebanks parseme/corpora@1.3.json \
		--request parseme/label_req.json \
		--clustering_key MWE.label \
		> html/tables/parseme/labels.json

parseme_all: parseme_valid parseme_label



label_upos_French-GSD:
	python3 build_table.py DC \
		--treebank "{\"SUD_French-GSD@latest\": \"${SUD}/SUD_French-GSD\"}" \
		--title "## edge label and dependant UPOS (SUD_French-GSD)" \
		--request "edge.req" \
		--row_key "e.label" \
		--col_key "N.ExtPos/upos" \
		> html/tables/SUD_French-GSD/label_upos.json

amb_lemma_French-GSD:
	python3 build_table.py DC \
		--treebank "{\"SUD_French-GSD@latest\": \"${SUD}/SUD_French-GSD\"}" \
		--title "## ambiguous lemmas UPOS (SUD_French-GSD@latest)" \
		--request "lemma.req" \
		--row_key "N.lemma" \
		--col_key "N.upos" \
		--filter \
		> html/tables/SUD_French-GSD/amb_lemma.json

pos_features_French-GSD:
	python3 pos_features.py \
		--treebank "{\"SUD_French-GSD@latest\": \"${SUD}/SUD_French-GSD\"}" \
		> html/tables/SUD_French-GSD/pos_features.json

all : stat_pos_features label_upos amb_lemma adj_lemma_pos parseme

stat_pos_features:
	mkdir -p html/_tables/SUD_Beja-NSC
	mkdir -p html/_tables/SUD_French-GSD
	mkdir -p html/_tables/SUD_French-Rhapsodie
	mkdir -p html/_tables/SUD_French-ParisStories
	mkdir -p html/_tables/PS_2023
	mkdir -p html/_tables/SUD_Naija-NSC
	mkdir -p html/_tables/SUD_Zaar-Autogramm
	python3 stat_pos_features.py SUD_Beja-NSC ${SUD}/SUD_Beja-NSC/*.conllu > html/_tables/SUD_Beja-NSC/stat_pos_features.json
	python3 stat_pos_features.py SUD_French-GSD ${SUD}/SUD_French-GSD/*.conllu > html/_tables/SUD_French-GSD/stat_pos_features.json
	python3 stat_pos_features.py SUD_French-Rhapsodie ${SUD}/SUD_French-Rhapsodie/*.conllu > html/_tables/SUD_French-Rhapsodie/stat_pos_features.json
	python3 stat_pos_features.py SUD_French-ParisStories ${SUD}/SUD_French-ParisStories/*.conllu > html/_tables/SUD_French-ParisStories/stat_pos_features.json
	python3 stat_pos_features.py PS_2023 ${SUD}/PS_2023/*.conllu > html/_tables/PS_2023/stat_pos_features.json
	python3 stat_pos_features.py SUD_Naija-NSC ${SUD}/SUD_Naija-NSC/*.conllu > html/_tables/SUD_Naija-NSC/stat_pos_features.json
	python3 stat_pos_features.py SUD_Zaar-Autogramm ${SUD}/SUD_Zaar-Autogramm/CORPUS/*.conllu > html/_tables/SUD_Zaar-Autogramm/stat_pos_features.json

label_upos:
	mkdir -p html/_tables/SUD_French-GSD
	mkdir -p html/_tables/SUD_French-Rhapsodie
	mkdir -p html/_tables/SUD_French-ParisStories
	mkdir -p html/_tables/PS_2023
	python3 double_clust.py label_upos SUD_French-GSD@latest ${SUD}/SUD_French-GSD/*.conllu > html/_tables/SUD_French-GSD/label_upos.json
	python3 double_clust.py label_upos SUD_French-Rhapsodie@latest ${SUD}/SUD_French-Rhapsodie/*.conllu > html/_tables/SUD_French-Rhapsodie/label_upos.json
	python3 double_clust.py label_upos SUD_French-ParisStories@latest ${SUD}/SUD_French-ParisStories/*.conllu > html/_tables/SUD_French-ParisStories/label_upos.json
	python3 double_clust.py label_upos PS_2023@latest ${SUD}/PS_2023/*.conllu > html/_tables/PS_2023/label_upos.json

amb_lemma:
	mkdir -p html/_tables/SUD_French-GSD
	mkdir -p html/_tables/SUD_French-Rhapsodie
	mkdir -p html/_tables/SUD_French-ParisStories
	mkdir -p html/_tables/PS_2023
	python3 double_clust.py amb_lemma SUD_French-GSD@latest ${SUD}/SUD_French-GSD/*.conllu > html/_tables/SUD_French-GSD/amb_lemma.json
	python3 double_clust.py amb_lemma SUD_French-Rhapsodie@latest ${SUD}/SUD_French-Rhapsodie/*.conllu > html/_tables/SUD_French-Rhapsodie/amb_lemma.json
	python3 double_clust.py amb_lemma SUD_French-ParisStories@latest ${SUD}/SUD_French-ParisStories/*.conllu > html/_tables/SUD_French-ParisStories/amb_lemma.json
	python3 double_clust.py amb_lemma PS_2023@latest ${SUD}/PS_2023/*.conllu > html/_tables/PS_2023/amb_lemma.json

adj_lemma_pos:
	mkdir -p html/_tables/SUD_French-GSD
	mkdir -p html/_tables/SUD_French-Rhapsodie
	mkdir -p html/_tables/SUD_French-ParisStories
	mkdir -p html/_tables/PS_2023
	python3 double_clust.py adj_lemma_pos SUD_French-GSD@latest ${SUD}/SUD_French-GSD/*.conllu > html/_tables/SUD_French-GSD/adj_lemma_pos.json
	python3 double_clust.py adj_lemma_pos SUD_French-Rhapsodie@latest ${SUD}/SUD_French-Rhapsodie/*.conllu > html/_tables/SUD_French-Rhapsodie/adj_lemma_pos.json
	python3 double_clust.py adj_lemma_pos SUD_French-ParisStories@latest ${SUD}/SUD_French-ParisStories/*.conllu > html/_tables/SUD_French-ParisStories/adj_lemma_pos.json
	python3 double_clust.py adj_lemma_pos PS_2023@latest ${SUD}/PS_2023/*.conllu > html/_tables/PS_2023/adj_lemma_pos.json

# parseme_old:
# 	mkdir -p html/_tables/parseme
# 	python3 parseme_by_label.py > html/_tables/parseme/lang_tags.json
# 	python3 parseme_validation.py > html/_tables/parseme/valid.json

sud:
	mkdir -p html/_tables/sud
	python3 multi_request.py > html/_tables/sud/subj_french.json

clean:
	rm -rf html/_tables