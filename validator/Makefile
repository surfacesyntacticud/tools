doc:
	@echo " * valid"
	@echo " * clean"
	@echo " * compile"

valid:
	grew_dev valid -pattern "modules/global.json modules/relations.json modules/obsolete.json modules/idioms.json modules/french_agreement.json" -i sud_fr.json -o ~/.local/www/grew/valid
	grew_dev valid -pattern "modules/global.json modules/relations.json modules/obsolete.json modules/idioms.json" -i sud_pcm.json -o ~/.local/www/grew/valid
	cp html/index.html ~/.local/www/grew/valid

clean:
	grew_dev clean -i sud_fr.json
	grew_dev clean -i sud_pcm.json

compile:
	grew_dev compile -i sud_fr.json
	grew_dev compile -i sud_pcm.json

gsd:
	open "http://localhost:8888/validator/?corpus=SUD_French-GSD@latest"
naija:
	open "http://localhost:8888/validator/?corpus=SUD_Naija-NSC@latest"