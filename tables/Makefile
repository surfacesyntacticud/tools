run:
	python3 ud_stat.py FEATS
	mv -f out.json FEATS.json
	python3 ud_stat.py MISC
	mv -f out.json MISC.json
	python3 ud_stat.py DEPS
	mv -f out.json DEPS.json

clean:
	rm -f FEATS.json MISC.json DEPS.json
