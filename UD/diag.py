#!/usr/bin/env python3
import sys
from collections import Counter

tests = [
	# SYNTAX
	("Unknown UPOS tag",":", ""),
	("Unknown DEPREL label",":", ""),
	("invalid-deprel", "]", ""),
	("right-to-left-goeswith", "]", ""),
	("goeswith-gap", "]", "["),
	("leaf-goeswith", "]", "("),
	("leaf-punct", "]", "("),
	("leaf-aux-cop", "]", "("),
	("leaf-det", "]", "("),
	("rel-upos-det", "]", "("),
	("rel-upos-cc", "]", "("),
	("rel-upos-aux", "]", "("),
	("rel-upos-cop", "]", "("),
	("rel-upos-expl", "]", "("),
	("rel-upos-punct", "]", "("),
	("rel-upos-nummod", "]", "("),
	("upos-rel-punct", "]", "("),
	("too-many-objects", "]", "["),
	("punct-causes-nonproj", "]", "["),
	("right-to-left-conj", "]", ""),
	("right-to-left-flat", "]", ""),
	("right-to-left-appos", "]", ""),
	("cop-lemma", "]", ""),

	# MORPHO
	("feature-value-unknown","]", ""),
	("goeswith-lemma", "]", ""),
	("goeswith-upos", "]", ""),
	("goeswith-missing-typo", "]", ""),
	("feature-value-upos-not-permitted", "]", "("),
	("feature-upos-not-permitted", "]", "("),
	("aux-lemma", "]", ""),

	# FORMAT
	("empty-column", "]", ":"),
	("trailing-whitespace", "]", ":"),
	("leading-whitespace", "]", ":"),
	("repeated-whitespace", "]", ":"),
	("invalid-word-with-space", "]", ""),

	# METADATA
	("missing-sent-id","]", ""),
	("invalid-sent-id","]", ":"),
	("spaceafter-value", "]", ""),
	("nospaceafter-yes", "]", ""),
	("non-unique-sent-id", "]", "'"),
]

def extract_after_second_sep(line: str, sep: str) -> str:
	parts = line.split(sep, 2)
	return parts[2].lstrip() if len(parts) == 3 else ""

def test(lines, text, sep, sep2):
	counts = Counter()
	for line in lines:
		if text in line:
			suff = extract_after_second_sep(line.rstrip("\n"), sep)
			if sep2:
				key = suff.split(sep2)[0]
			else:
				key = suff
			if key:
				counts[key] += 1
	if len (counts) > 0:
		print (f"========== {text} ==========")
		for item, cnt in counts.most_common():
			print(f"{cnt:7d} {item}")

def main(path):
	with open(path, "r", encoding="utf-8") as f:
		lines = f.readlines()
	for (name, sep1, sep2) in tests:
		test (lines, name, sep1, sep2)

	def keep (line):
		if not line.startswith("[Line"): return False
		keep = True
		for (test,_,_) in tests:
			if test in line:
				keep = False
				break
		return keep

	others_lines = [line for line in lines if keep (line)]
	if len(others_lines) > 0:
		print (f"========== Other errors ==========")
	for line in others_lines:
		print (line.strip())

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python3 diag.py input_file", file=sys.stderr)
		sys.exit(1)
	main(sys.argv[1])
