UD=/users/guillaum/resources/ud-treebanks-v2.10
SUD=/users/guillaum/resources/sud-treebanks-v2.10

FEAT_LIST=PronType Gender VerbForm NumType Animacy Mood Poss NounClass Tense Reflex Number Aspect Foreign Case Voice Abbr Definite Evident Typo Degree Polarity Person Polite Clusivity
UD_LIST=acl advcl advmod amod appos aux case cc ccomp clf compound conj cop csubj dep det discourse dislocated expl fixed flat goeswith iobj list mark nmod nsubj nummod obj obl orphan parataxis punct reparandum root vocative xcomp
SUD_LIST=unk subj udep mod comp vocative dislocated discourse appos det clf conj cc flat compound list parataxis orphan goeswith reparandum punct

FILTER=*UD_*

selfdoc:
	@echo "make all"
	@echo "make build_sud_deps"
	@echo "make build_ud_deps"
	@echo "make build_ud_feats"
	@echo "make build_meta"
	@echo "make count"


all: build_sud_deps build_ud_deps build_ud_feats build_meta count

count:
	python count.py

build_meta:
	mkdir -p meta
	python build_table.py -c "UD 2.10" -f "${FILTER}" -o meta/META.json ${UD} META

build_sud_deps:
	mkdir -p sud_deps
	python build_table.py -c "SUD 2.10" -f "${FILTER}" -o sud_deps/DEPS.json ${SUD} DEPS
	python build_table.py -c "SUD 2.10" -f "${FILTER}" -o sud_deps/UDEPS.json ${SUD} UDEPS
	python build_table.py -c "SUD 2.10" -f "${FILTER}" -o sud_deps/DEEP.json ${SUD} DEEP
	@for udep in ${SUD_LIST} ; do \
		echo "================= Building table for udep: $$udep =================" ; \
		python build_table.py -c "SUD 2.10" -f "${FILTER}" -o sud_deps/$$udep.json ${SUD} SUBREL:$$udep ; \
	done

build_ud_deps:
	mkdir -p ud_deps
	python build_table.py -c "UD 2.10" -f "${FILTER}" -o ud_deps/DEPS.json ${UD} DEPS
	python build_table.py -c "UD 2.10" -f "${FILTER}" -o ud_deps/UDEPS.json ${UD} UDEPS
	@for udep in ${UD_LIST} ; do \
		echo "================= Building table for udep: $$udep =================" ; \
		python build_table.py -c "UD 2.10" -f "${FILTER}" -o ud_deps/$$udep.json ${UD} SUBREL:$$udep ; \
	done

build_ud_feats:
	mkdir -p ud_feats
	python build_table.py -c "UD 2.10" -f "${FILTER}" -o ud_feats/FEATS.json ${UD} FEATS
	python build_table.py -c "UD 2.10" -f "${FILTER}" -o ud_feats/MISC.json ${UD} MISC
	@for feat in ${FEAT_LIST} ; do \
		echo "================= Building table for feature: $$feat =================" ; \
		python build_table.py -c "UD 2.10" -f "${FILTER}" -o ud_feats/$$feat.json ${UD} FEAT:$$feat ; \
	done

purge:
	rm -rf ud_feats
	rm -rf ud_deps
	rm -rf sud_deps
	rm -rf meta
	rm -f count.json

start:
	python -m http.server &
	open "http://localhost:8000?data=ud/feats"

stop:
	kill `lsof -t -i :8000`
