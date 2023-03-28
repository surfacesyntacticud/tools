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

all : stat_pos_features label_upos amb_lemma adj_lemma_pos parseme

stat_pos_features:
	mkdir -p html/_tables/SUD_Beja-NSC
	mkdir -p html/_tables/SUD_French-GSD
	mkdir -p html/_tables/SUD_French-Rhapsodie
	mkdir -p html/_tables/SUD_French-ParisStories
	mkdir -p html/_tables/SUD_Naija-NSC
	mkdir -p html/_tables/SUD_Zaar-Autogramm
	python3 stat_pos_features.py SUD_Beja-NSC ${SUD}/SUD_Beja-NSC/*.conllu > html/_tables/SUD_Beja-NSC/stat_pos_features.json
	python3 stat_pos_features.py SUD_French-GSD ${SUD}/SUD_French-GSD/*.conllu > html/_tables/SUD_French-GSD/stat_pos_features.json
	python3 stat_pos_features.py SUD_French-Rhapsodie ${SUD}/SUD_French-Rhapsodie/*.conllu > html/_tables/SUD_French-Rhapsodie/stat_pos_features.json
	python3 stat_pos_features.py SUD_French-ParisStories ${SUD}/SUD_French-ParisStories/*.conllu > html/_tables/SUD_French-ParisStories/stat_pos_features.json
	python3 stat_pos_features.py SUD_Naija-NSC ${SUD}/SUD_Naija-NSC/*.conllu > html/_tables/SUD_Naija-NSC/stat_pos_features.json
	python3 stat_pos_features.py SUD_Zaar-Autogramm ${SUD}/SUD_Zaar-Autogramm/CORPUS/*.conllu > html/_tables/SUD_Zaar-Autogramm/stat_pos_features.json

label_upos:
	mkdir -p html/_tables/SUD_French-GSD
	mkdir -p html/_tables/SUD_French-Rhapsodie
	mkdir -p html/_tables/SUD_French-ParisStories
	python3 double_clust.py label_upos SUD_French-GSD@latest ${SUD}/SUD_French-GSD/*.conllu > html/_tables/SUD_French-GSD/label_upos.json
	python3 double_clust.py label_upos SUD_French-Rhapsodie@latest ${SUD}/SUD_French-Rhapsodie/*.conllu > html/_tables/SUD_French-Rhapsodie/label_upos.json
	python3 double_clust.py label_upos SUD_French-ParisStories@latest ${SUD}/SUD_French-ParisStories/*.conllu > html/_tables/SUD_French-ParisStories/label_upos.json

amb_lemma:
	mkdir -p html/_tables/SUD_French-GSD
	mkdir -p html/_tables/SUD_French-Rhapsodie
	mkdir -p html/_tables/SUD_French-ParisStories
	python3 double_clust.py amb_lemma SUD_French-GSD@latest ${SUD}/SUD_French-GSD/*.conllu > html/_tables/SUD_French-GSD/amb_lemma.json
	python3 double_clust.py amb_lemma SUD_French-Rhapsodie@latest ${SUD}/SUD_French-Rhapsodie/*.conllu > html/_tables/SUD_French-Rhapsodie/amb_lemma.json
	python3 double_clust.py amb_lemma SUD_French-ParisStories@latest ${SUD}/SUD_French-ParisStories/*.conllu > html/_tables/SUD_French-ParisStories/amb_lemma.json

adj_lemma_pos:
	mkdir -p html/_tables/SUD_French-GSD
	mkdir -p html/_tables/SUD_French-Rhapsodie
	mkdir -p html/_tables/SUD_French-ParisStories
	python3 double_clust.py adj_lemma_pos SUD_French-GSD@latest ${SUD}/SUD_French-GSD/*.conllu > html/_tables/SUD_French-GSD/adj_lemma_pos.json
	python3 double_clust.py adj_lemma_pos SUD_French-Rhapsodie@latest ${SUD}/SUD_French-Rhapsodie/*.conllu > html/_tables/SUD_French-Rhapsodie/adj_lemma_pos.json
	python3 double_clust.py adj_lemma_pos SUD_French-ParisStories@latest ${SUD}/SUD_French-ParisStories/*.conllu > html/_tables/SUD_French-ParisStories/adj_lemma_pos.json

parseme:
	mkdir -p html/_tables/parseme
	python3 multi_ling.py > html/_tables/parseme/lang_tags.json

sud:
	mkdir -p html/_tables/sud
	python3 multi_request.py > html/_tables/sud/subj_french.json

clean:
	rm -rf html/_tables