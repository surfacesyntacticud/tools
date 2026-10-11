import sys, json
from pathlib import Path
from termcolor import colored, cprint
from grewpy import Corpus, Request, CorpusDraft, set_config

set_config("sud")

cpt_files=0 # counter for produced files
cpt_trees=0 # counter for produced sentences
cpt_sents=0 # counter for all sentences

def extract_file (infile, outfile):
	global cpt_files, cpt_trees, cpt_sents
	corpus = Corpus (infile)
	cpt_sents += len(corpus)
	r = Request ("pattern { global.is_tree }")

	tree_ids = [m["sent_id"] for m in corpus.search(r)]

	if len(tree_ids) > 0:
		tree_ids.reverse()
		trees = CorpusDraft()
		for tree_id in tree_ids:
			trees[tree_id] = corpus[tree_id]
		with open(outfile, "w") as f:
			f.write(trees.to_conll ())
		cpt_files += 1
		cpt_trees += len(tree_ids)
		cprint (f"file `{infile}` --> {len(tree_ids)}/{len(corpus)}", "green" if len(tree_ids) == len(corpus) else "blue")
	else:
		cprint (f"no trees in file `{infile}`", "yellow")


if __name__ == "__main__":
	if len(sys.argv) != 3:
		cprint ("2 args needed", "red")
		sys.exit (1)
	input_path = Path(sys.argv[1])
	output_path = Path(sys.argv[2])
	if not input_path.is_dir():
		cprint (f"first arg `{sys.argv[1]}` is not a folder", "red")
		sys.exit (1)
	output_path.mkdir(exist_ok=True)
	cpt_infiles = 0
	for input_file in input_path.glob('*.conllu'):
		cpt_infiles += 1
		output_file = output_path / input_file.name
		extract_file(str(input_file), str(output_file))
	print ("-------------------")
	cprint (f"files     --> {cpt_files}/{cpt_infiles}", "green")
	cprint (f"sentences --> {cpt_trees}/{cpt_sents}", "green")