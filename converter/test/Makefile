DATE=`date`

draw:
	@make -C basic draw
	@make -C coord draw
	@make -C gsd draw
	@make -C sequoia draw
	@make -C web draw
	@make -C impersonal_diathesis draw
	@make -C pronominal_verbs draw
	pandoc --metadata title="$(DATE)" -s -c github-pandoc.css diff.md -o index.html

clean:
	@make -C basic clean
	@make -C coord clean
	@make -C gsd clean
	@make -C sequoia clean
	@make -C web clean
	@make -C impersonal_diathesis clean
	@make -C pronominal_verbs clean
	rm -f index.html

lchn:
	scp -r index.html github-pandoc.css \
	basic \
	coord \
	gsd \
	sequoia \
	web \
	impersonal_diathesis \
	pronominal_verbs \
	$(slchn)/www/download/UD_SUD/