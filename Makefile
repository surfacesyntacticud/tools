doc:
	@echo "run: transform dev-GSD"
	@echo "gui: run GUI on dev-GSD"

run:
	grew_dev transform -grs ud_surf.grs -i UD_French-GSD/fr_gsd-ud-dev.conllu -o dev_surf.conllu
	grew_dev transform -grs ud_surf.grs -i UD_French-GSD/fr_gsd-ud-test.conllu -o test_surf.conllu
	grew_dev transform -grs ud_surf.grs -i UD_French-GSD/fr_gsd-ud-train.conllu -o train_surf.conllu

gui:
	grew_dev gui -grs ud_surf.grs -i UD_French-GSD/fr_gsd-ud-dev.conllu

clean:
	rm -f dev_surf.conllu
