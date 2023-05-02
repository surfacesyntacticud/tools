doc:
	@echo " * valid    --> Run validation on native SUD"
	@echo " * clean    --> Clean corpora"
	@echo " * compile  --> Compile corpora"
	@echo " * url      --> Show local URLs"

valid:
	# remove old validations
	rm -f ~/.local/www/grew/valid/*.json
	grew_dev valid -pattern "modules/global.json modules/relations.json modules/obsolete.json modules/idioms.json modules/french_agreement.json" -i sud_fr.json -o ~/.local/www/grew/valid
	grew_dev valid -pattern "modules/global.json modules/relations.json modules/obsolete.json modules/idioms.json modules/zh_char.json" -i sud_zh.json -o ~/.local/www/grew/valid
	grew_dev valid -pattern "modules/global.json modules/relations.json modules/obsolete.json modules/idioms.json" -i sud_pcm.json -o ~/.local/www/grew/valid
	cp html/index.html ~/.local/www/grew/valid

clean:
	grew_dev clean -i sud_fr.json
	grew_dev clean -i sud_pcm.json

compile:
	grew_dev compile -i sud_fr.json
	grew_dev compile -i sud_pcm.json

url:
	@echo "http://localhost:8888/validator/?corpus=SUD_French-GSD@latest"
	@echo "http://localhost:8888/validator/?corpus=SUD_French-Rhapsodie@latest"
	@echo "http://localhost:8888/validator/?corpus=SUD_French-ParisStories@latest"
	@echo "http://localhost:8888/validator/?corpus=SUD_Naija-NSC@latest"