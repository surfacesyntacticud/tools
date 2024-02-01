build:
	python3 ../make_syllabes.py sud.conllu sud_syllable.conllu
	grew transform -config sud -grs ../fused.grs -i sud_syllable.conllu -o sud_fused.conllu
	dep2pict sud.conllu sud.svg
	dep2pict sud_syllable.conllu sud_syllable.svg
	dep2pict sud_fused.conllu sud_fused.svg
