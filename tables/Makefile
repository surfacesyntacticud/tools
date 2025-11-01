UD=/users/guillaum/resources/ud-treebanks-v2.16
SUD=/users/guillaum/resources/sud-treebanks-v2.16
SP_UD=/users/guillaum/resources/SP_ud-treebanks-v2.16

FEAT_LIST=PronType Gender VerbForm NumType Animacy Mood Poss NounClass Tense Reflex Number Aspect Foreign Case Voice Abbr Definite Evident Typo Degree Polarity Person Polite Clusivity ExtPos Deixis DeixisRef
UD_LIST=acl advcl advmod amod appos _aux case cc ccomp clf compound conj cop csubj dep det discourse dislocated expl fixed flat goeswith iobj list mark nmod nsubj nummod obj obl orphan parataxis punct reparandum root vocative xcomp
SUD_LIST=unk subj udep mod comp vocative dislocated discourse appos det clf conj cc flat compound list parataxis orphan goeswith reparandum punct

FILTER=*UD_*

selfdoc:
	@echo "make all"
	@echo "make build_sud_deps"
	@echo "make build_ud_deps"
	@echo "make build_ud_feats"
	@echo "make build_meta"
	@echo "make build_SP_ud_deps"
	@echo "make build_SP_ud_feats"
	@echo "make build_SP_meta"
	@echo "make count"

univ: build_sud_deps build_ud_deps build_ud_feats build_meta count
spoken: build_SP_meta build_SP_ud_deps build_SP_ud_feats count
all: univ spoken

count:
	python count.py

build_meta:
	mkdir -p meta
	python build_table.py -c "UD 2.16" -f "${FILTER}" -o meta/META.json ${UD} META

build_SP_meta:
	mkdir -p SP_meta
	python build_table.py --instance spoken --prefix "SP_" -c "SP_UD 2.16" -f "${FILTER}" -o SP_meta/META.json ${SP_UD} META

build_sud_deps:
	mkdir -p sud_deps
	python build_table.py -c "SUD 2.16" -f "${FILTER}" -o sud_deps/DEPS.json ${SUD} DEPS
	python build_table.py -c "SUD 2.16" -f "${FILTER}" -o sud_deps/UDEPS.json ${SUD} UDEPS
	python build_table.py -c "SUD 2.16" -f "${FILTER}" -o sud_deps/DEEP.json ${SUD} DEEP
	@for udep in ${SUD_LIST} ; do \
		echo "================= Building table for udep: $$udep =================" ; \
		python build_table.py -c "SUD 2.16" -f "${FILTER}" -o sud_deps/$$udep.json ${SUD} SUBREL:$$udep ; \
	done

build_ud_deps:
	mkdir -p ud_deps
	python build_table.py -c "UD 2.16" -f "${FILTER}" -o ud_deps/DEPS.json ${UD} DEPS
	python build_table.py -c "UD 2.16" -f "${FILTER}" -o ud_deps/UDEPS.json ${UD} UDEPS
	@for udep in ${UD_LIST} ; do \
		echo "================= Building table for udep: $$udep =================" ; \
		python build_table.py -c "UD 2.16" -f "${FILTER}" -o ud_deps/$$udep.json ${UD} SUBREL:$$udep ; \
	done

build_SP_ud_deps:
	mkdir -p SP_ud_deps
	python build_table.py --instance spoken --prefix "SP_" -c "SP_UD 2.16" -f "${FILTER}" -o SP_ud_deps/DEPS.json ${SP_UD} DEPS
	python build_table.py --instance spoken --prefix "SP_" -c "SP_UD 2.16" -f "${FILTER}" -o SP_ud_deps/UDEPS.json ${SP_UD} UDEPS
	@for udep in ${UD_LIST} ; do \
		echo "================= Building table for udep: $$udep =================" ; \
		python build_table.py --instance spoken --prefix "SP_" -c "SP_UD 2.16" -f "${FILTER}" -o SP_ud_deps/$$udep.json ${SP_UD} SUBREL:$$udep ; \
	done

build_ud_feats:
	mkdir -p ud_feats
	python build_table.py -c "UD 2.16" -f "${FILTER}" -o ud_feats/FEATS.json ${UD} FEATS
	python build_table.py -c "UD 2.16" -f "${FILTER}" -o ud_feats/MISC.json ${UD} MISC
	@for feat in ${FEAT_LIST} ; do \
		echo "================= Building table for feature: $$feat =================" ; \
		python build_table.py -c "UD 2.16" -f "${FILTER}" -o ud_feats/$$feat.json ${UD} FEAT:$$feat ; \
	done

build_SP_ud_feats:
	mkdir -p SP_ud_feats
	python build_table.py --instance spoken --prefix "SP_" -c "SP_UD 2.16" -f "${FILTER}" -o SP_ud_feats/FEATS.json ${SP_UD} FEATS
	python build_table.py --instance spoken --prefix "SP_" -c "SP_UD 2.16" -f "${FILTER}" -o SP_ud_feats/MISC.json ${SP_UD} MISC
	@for feat in ${FEAT_LIST} ; do \
		echo "================= Building table for feature: $$feat =================" ; \
		python build_table.py --instance spoken --prefix "SP_" -c "SP_UD 2.16" -f "${FILTER}" -o SP_ud_feats/$$feat.json ${SP_UD} FEAT:$$feat ; \
	done

purge:
	rm -rf ud_feats
	rm -rf ud_deps
	rm -rf sud_deps
	rm -rf SP_ud_feats
	rm -rf SP_ud_deps
	rm -rf meta
	rm -rf SP_meta
	rm -f count.json

start:
	python -m http.server &
	open "http://localhost:8000?data=ud/feats"

stop:
	kill `lsof -t -i :8000`
