import sys

def parse_misc(m):
  d = dict()
  for feat in m.split("|"):
    e = feat.find('=')
    d[feat[0:e]] = feat[e+1:]
  return d

infile = sys.argv[1]
with open(infile, 'r') as f:
  lines = f.readlines()

outfile = sys.argv[2] if len(sys.argv) > 2 else None
with open(outfile, "w") if outfile else sys.stdout as f:
  for line in lines:
    l = line.strip()
    if l == "":
      f.write(l+"\n")
    elif l[0] == "#":
      f.write(l+"\n")
    else:
      fields = line.split("\t")
      feats = parse_misc(fields[9])
      reduced_feats = { k: feats[k] for k in feats if not k.startswith("Syl") }
      misc = "|".join([f"{k}={reduced_feats[k]}" for k in reduced_feats])
      f.write("\t".join(fields[0:9])+"\t"+misc.strip()+"\n")
      cont = True
      pos = 1
      while cont:
        prefix = f"Syl{pos}"
        subfeats = { k: feats[k] for k in feats if k.startswith(prefix) }
        if len(subfeats) == 0:
          cont=False
        else:
          misc_list = [f"{k[4:]}={subfeats[k]}" for k in subfeats if k != prefix]
          misc = "|".join(misc_list)
          # Some numeric features can occasionaly have value "X" like "MeanF0=X"
          # This value is not accepted by Grew, so it is replaced by "MeanF0_X=Yes"
          misc = misc.replace("MeanF0=X", "MeanF0_X=Yes")
          misc = misc.replace("Duration=X", "Duration_X=Yes")
          misc = misc.replace("MaxAmplitude=X", "MaxAmplitude_X=Yes")
          misc = misc.replace("AvgAmplitude=X", "AvgAmplitude_X=Yes")
          if misc == "":
            misc = "_"
          syl_id = f"{fields[0]}.{pos}"
          form = subfeats.get(prefix, "__undef__").strip()
          if form == "":
            form = "__empty__"
          f.write(f"{syl_id}\t_\t_\t_\t_\tSylForm={form}\t{fields[0]}\tSyl={pos}\t_\t{misc}\n")
          pos += 1
