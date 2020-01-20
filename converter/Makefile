doc:
	@echo "----------------------------------"
	@echo "gsd_sud:      convert GSD  in SUD "
	@echo ""
	@echo "See in experiment for more targets"
	@echo "----------------------------------"

DATE=`date "+%Y_%m_%d_%H_%M_%S"`
conv:
	mkdir sud_${DATE}
	for file in ud/UD*/*test.conllu
		do @echo ${file}
	done

gsd_sud:
	grew transform -grs grs/UD_to_SUD_fr.grs -strat FR_main -i UD_French-GSD/not-to-release/fr_gsd-ud-dev.conllu -o _fr_gsd-ud-dev.sud.conllu
	grew transform -grs grs/UD_to_SUD_fr.grs -strat FR_main -i UD_French-GSD/not-to-release/fr_gsd-ud-test.conllu -o _fr_gsd-ud-test.sud.conllu
	grew transform -grs grs/UD_to_SUD_fr.grs -strat FR_main -i UD_French-GSD/not-to-release/fr_gsd-ud-train.conllu -o _fr_gsd-ud-train.sud.conllu

gsd_old:
	grew transform -grs grs/UD_to_SUD_fr.grs -strat FR_old -i UD_French-GSD/not-to-release/fr_gsd-ud-dev.conllu -o _fr_gsd-ud-dev.old.conllu
	grew transform -grs grs/UD_to_SUD_fr.grs -strat FR_old -i UD_French-GSD/not-to-release/fr_gsd-ud-test.conllu -o _fr_gsd-ud-test.old.conllu
	grew transform -grs grs/UD_to_SUD_fr.grs -strat FR_old -i UD_French-GSD/not-to-release/fr_gsd-ud-train.conllu -o _fr_gsd-ud-train.old.conllu

gui:
	grew gui -grs grs/UD_to_SUD.grs -i UD_French-GSD/fr_gsd-ud-dev.conllu

dc:
	grew transform -grs grs/UD_to_SUD.grs -i UD_French-GSD/fr_gsd-ud-dev.conllu -o _fr_gsd-ud-dev.sud.conllu
	grew transform -grs grs/SUD_to_UD.grs -i _fr_gsd-ud-dev.sud.conllu -o _fr_gsd-ud-dev.dc.conllu

dc2:
	grew transform -grs grs/UD_to_SUD.grs -i UD_French-GSD/fr_gsd-ud-dev.conllu -o _fr_gsd-ud-dev.sud2.conllu
	grew transform -grs grs/SUD_to_UD.grs -i _fr_gsd-ud-dev.sud2.conllu -o _fr_gsd-ud-dev.dc2.conllu

clean:
	rm -rf _*

.SUFFIXES: .svg .conll

.conll.svg:
	dep2pict $< $@

ja:
	grew transform -grs grs/UD_to_SUD.grs -i ja_ud.conll -o _ja_sud_conv.conll

ja_gui:
	grew gui -grs UD_to_SUD.grs -i ja_ud.conll

gum:
	grew gui -grs grs/UD_to_SUD.grs -i  /users/guillaum/resources/ud-treebanks-v2.4/UD_English-GUM/en_gum-ud-train.conllu

dev:
	grew transform -grs grs/UD_to_SUD.grs -i UD_French-GSD/fr_gsd-ud-dev.conllu -o _fr_gsd-ud-dev.sud.conllu
