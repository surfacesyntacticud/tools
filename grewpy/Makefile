SUD=/Users/guillaum/github/surfacesyntacticud

stat_pos_features:
	python3 stat_pos_features.py SUD_Beja-NSC ${SUD}/SUD_Beja-NSC/*.conllu > tables/SUD_Beja-NSC/stat_pos_features.json
	python3 stat_pos_features.py SUD_French-GSD ${SUD}/SUD_French-GSD/*.conllu > tables/SUD_French-GSD/stat_pos_features.json
	python3 stat_pos_features.py SUD_French-Rhapsodie ${SUD}/SUD_French-Rhapsodie/*.conllu > tables/SUD_French-Rhapsodie/stat_pos_features.json
	python3 stat_pos_features.py SUD_French-ParisStories ${SUD}/SUD_French-ParisStories/*.conllu > tables/SUD_French-ParisStories/stat_pos_features.json
	python3 stat_pos_features.py SUD_Naija-NSC ${SUD}/SUD_Naija-NSC/*.conllu > tables/SUD_Naija-NSC/stat_pos_features.json
	python3 stat_pos_features.py SUD_Zaar-Autogramm ${SUD}/SUD_Zaar-Autogramm/CORPUS/*.conllu > tables/SUD_Zaar-Autogramm/stat_pos_features.json

label_upos:
	python3 double_clust.py label_upos SUD_French-GSD@latest ${SUD}/SUD_French-GSD/*.conllu > tables/SUD_French-GSD/label_upos.json
	python3 double_clust.py label_upos SUD_French-Rhapsodie@latest ${SUD}/SUD_French-Rhapsodie/*.conllu > tables/SUD_French-Rhapsodie/label_upos.json
	python3 double_clust.py label_upos SUD_French-ParisStories@latest ${SUD}/SUD_French-ParisStories/*.conllu > tables/SUD_French-ParisStories/label_upos.json

amb_lemma:
	python3 double_clust.py amb_lemma SUD_French-GSD@latest ${SUD}/SUD_French-GSD/*.conllu > tables/SUD_French-GSD/amb_lemma.json
	python3 double_clust.py amb_lemma SUD_French-Rhapsodie@latest ${SUD}/SUD_French-Rhapsodie/*.conllu > tables/SUD_French-Rhapsodie/amb_lemma.json
	python3 double_clust.py amb_lemma SUD_French-ParisStories@latest ${SUD}/SUD_French-ParisStories/*.conllu > tables/SUD_French-ParisStories/amb_lemma.json

adj_lemma_pos:
	python3 double_clust.py adj_lemma_pos SUD_French-GSD@latest ${SUD}/SUD_French-GSD/*.conllu > tables/SUD_French-GSD/adj_lemma_pos.json
	python3 double_clust.py adj_lemma_pos SUD_French-Rhapsodie@latest ${SUD}/SUD_French-Rhapsodie/*.conllu > tables/SUD_French-Rhapsodie/adj_lemma_pos.json
	python3 double_clust.py adj_lemma_pos SUD_French-ParisStories@latest ${SUD}/SUD_French-ParisStories/*.conllu > tables/SUD_French-ParisStories/adj_lemma_pos.json

