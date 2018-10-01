doc:
	@echo "----------------------------------"
	@echo "gsd_sud:      convert GSD  in SUD "
	@echo ""
	@echo "See in experiment for more targets"
	@echo "----------------------------------"


gsd_sud:
	grew transform -grs UD_to_SUD.grs -i UD_French-GSD/fr_gsd-ud-dev.conllu -o _fr_gsd-ud-dev.sud.conllu
	grew transform -grs UD_to_SUD.grs -i UD_French-GSD/fr_gsd-ud-test.conllu -o _fr_gsd-ud-test.sud.conllu
	grew transform -grs UD_to_SUD.grs -i UD_French-GSD/fr_gsd-ud-train.conllu -o _fr_gsd-ud-train.sud.conllu

clean:
	rm -rf _*

.SUFFIXES: .svg .conll

.conll.svg:
	dep2pict $< $@

ja:
	grew transform -grs UD_to_SUD.grs -i ja_ud.conll -o _ja_sud_conv.conll

ja_gui:
	grew gui -grs UD_to_SUD.grs -i ja_ud.conll

