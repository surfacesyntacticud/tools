doc:
	@echo "----------------------------------------------------------------"
	@echo "sud:     convert ud.conll into _sud_conv.conll and show diff"
	@echo "ud:      convert sud.conll into _ud_conv.conll and show diff"
	@echo ""
	@echo "gui_ud:  run GUI on SUD_to_UD conversion"
	@echo "gui_sud: run GUI on UD_to_SUD conversion"
	@echo ""
	@echo "draw_ud: convert sud.conll into _ud_conv.conll and build figures"
	@echo "----------------------------------------------------------------"

sud:
	grew_dev transform -grs UD_to_SUD.grs -i ud.conll -o _sud_conv.conll
	opendiff sud.conll _sud_conv.conll

ud:
	grew_dev transform -grs SUD_to_UD.grs -i sud.conll -o _ud_conv.conll
	opendiff ud.conll _ud_conv.conll

gui_ud:
	grew_dev gui -grs SUD_to_UD.grs -i sud.conll

gui_sud:
	grew_dev gui -grs UD_to_SUD.grs -i ud.conll

draw_ud:
	grew_dev transform -grs SUD_to_UD.grs -i sud.conll -o _ud_conv.conll
	rm -rf _sud
	splitter sud.conll _sud
	find _sud -name "*.conll" -type f -print | sed "s/.conll$$//" | xargs -I {} make "{}.svg"
	rm -rf _ud_conv
	splitter _ud_conv.conll _ud_conv
	find _ud_conv -name "*.conll" -type f -print | sed "s/.conll$$//" | xargs -I {} make "{}.svg"

gsd_sud:
	grew_dev transform -grs UD_to_SUD.grs -i UD_French-GSD/fr_gsd-ud-dev.conllu -o _fr_gsd-ud-dev.sud.conllu
	grew_dev transform -grs UD_to_SUD.grs -i UD_French-GSD/fr_gsd-ud-test.conllu -o _fr_gsd-ud-test.sud.conllu
	grew_dev transform -grs UD_to_SUD.grs -i UD_French-GSD/fr_gsd-ud-train.conllu -o _fr_gsd-ud-train.sud.conllu

clean:
	rm -rf _*

.SUFFIXES: .svg .conll

.conll.svg:
	dep2pict $< $@

