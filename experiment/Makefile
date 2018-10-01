doc:
	@echo "----------------------------------------------------------------"
	@echo "sud:     convert ud.conll into _sud_conv.conll and show diff"
	@echo "ud:      convert sud.conll into _ud_conv.conll and show diff"
	@echo ""
	@echo "gui_ud:  run GUI on SUD_to_UD conversion"
	@echo "gui_sud: run GUI on UD_to_SUD conversion"
	@echo ""
	@echo "draw:    run both convertion build figures"
	@echo "----------------------------------------------------------------"

draw:
	rm -rf _sud_gold
	splitter sud.conll _sud_gold
	find _sud_gold -name "*.conll" -type f -print | sed "s/.conll$$//" | xargs -I {} make "{}.svg"
	grew transform -grs ../grs/SUD_to_UD.grs -i sud.conll -o _ud.conll
	rm -rf _ud_auto
	splitter _ud.conll _ud_auto
	# ----
	rm -rf _ud_gold
	splitter ud.conll _ud_gold
	find _ud_gold -name "*.conll" -type f -print | sed "s/.conll$$//" | xargs -I {} make "{}.svg"
	grew transform -grs ../grs/UD_to_SUD.grs -i ud.conll -o _sud.conll
	rm -rf _sud_auto
	splitter _sud.conll _sud_auto
	# ----
	dep_diff -d1 _sud_gold -d2 _sud_auto -svg _sud_diff
	dep_diff -d1 _ud_gold -d2 _ud_auto -svg _ud_diff

install:
	cp -f _sud_diff/* /users/guillaum/gitlab/grew/grew_doc/static/_sud_diff/
	cp -f _ud_diff/* /users/guillaum/gitlab/grew/grew_doc/static/_ud_diff/

gui_ud:
	grew gui -grs ../grs/SUD_to_UD.grs -i sud.conll

gui_sud:
	grew gui -grs ../grs/UD_to_SUD.grs -i ud.conll

sud:
	grew transform -grs ../grs/UD_to_SUD.grs -i ud.conll -o _sud_conv.conll
	opendiff sud.conll _sud_conv.conll

ud:
	grew transform -grs ../grs/SUD_to_UD.grs -i sud.conll -o _ud_conv.conll
	opendiff ud.conll _ud_conv.conll

full_ud:
	grew transform -grs ../grs/SUD_to_UD.grs -strat full -i sud.conll -o _ud_full_conv.conll

clean:
	rm -rf _*

.SUFFIXES: .svg .conll

.conll.svg:
	dep2pict $< $@

