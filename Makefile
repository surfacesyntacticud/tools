doc:
	@echo "conv: convert sud.conll into UD and build figures"
	@echo "gui: run GUI on sud.conll"

gui:
	grew_dev gui -grs SUD_to_UD.grs -i sud_examples.conll

conv:
	grew_dev transform -grs SUD_to_UD.grs -i sud.conll -o _ud_conv.conll
	rm -rf _sud
	splitter sud.conll _sud
	find _sud -name "*.conll" -type f -print | sed "s/.conll$$//" | xargs -I {} make "{}.svg"
	rm -rf _ud_conv
	splitter _ud_conv.conll _ud_conv
	find _ud_conv -name "*.conll" -type f -print | sed "s/.conll$$//" | xargs -I {} make "{}.svg"

run_UD_to_SUD:
	grew_dev transform -grs UD_to_SUD.grs -i UD_French-GSD/fr_gsd-ud-dev.conllu -o dev_surf.conllu
	grew_dev transform -grs UD_to_SUD.grs -i UD_French-GSD/fr_gsd-ud-test.conllu -o test_surf.conllu
	grew_dev transform -grs UD_to_SUD.grs -i UD_French-GSD/fr_gsd-ud-train.conllu -o train_surf.conllu

gui_UD_to_SUD:
	grew_dev gui -grs UD_to_SUD.grs -i UD_French-GSD/fr_gsd-ud-dev.conllu

clean:
	rm -rf _*

.SUFFIXES: .svg .conll

.conll.svg:
	dep2pict $< $@
