import math

from grewpy import Request, Corpus

corpus = Corpus ("SUD_Naija-NSC-prosody")

request = Request.parse ("""
pattern {
  GO1 -[comp:aux]-> GO2;
  GO1 [form="go"]; GO2 [form="go"];
  GO1 -[Syl=1]-> S1; GO2 -[Syl=1]-> S2
}
""")

occurrences = corpus.search(request)

for occ in occurrences:
	print (occ["sent_id"])
	graph = corpus[occ["sent_id"]]
	S1 = graph[occ["matching"]["nodes"]["S1"]]
	S2 = graph[occ["matching"]["nodes"]["S2"]]
	f1 = float(S1["MeanF0"]) if "MeanF0" in S1 else None
	f2 = float(S2["MeanF0"]) if "MeanF0" in S2 else None
	if f1 and f2:
		st = 12 * math.log2(f2/f1)
		print (f"st = {st}")
	else:
		print ("Missing MeanF0")
