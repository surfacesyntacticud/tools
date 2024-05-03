import sys

def parse_misc(m):
  d = dict()
  for feat in m.split("|"):
    e = feat.find('=')
    d[feat[0:e]] = feat[e+1:]
  return d

with open(sys.argv[1], 'r') as f:
  lines = f.readlines()

with open(sys.argv[2], "w") if len(sys.argv)>2 else sys.stdout as f:
  for line in lines:
    if line.strip() == "" or line[0] == "#":
      f.write(line)
    else:
      fields = line.strip().split("\t")
      feats = parse_misc(fields[9])
      word_feats = { k: feats[k] for k in feats if not k.startswith("Syl") }
      word_misc = "|".join([f"{k}={word_feats[k]}" for k in word_feats])
      f.write("\t".join(fields[0:9])+"\t"+word_misc+"\n")
      done = False
      syl_number = 1
      while not done:
        prefix = f"Syl{syl_number}"
        syl_feats = { k: feats[k] for k in feats if k.startswith(prefix) }
        if len(syl_feats) == 0:
          done=True
        else:
          syl_misc = "|".join([f"{k[4:]}={syl_feats[k]}" for k in syl_feats if k != prefix])
          # Some numeric features can occasionaly have value "X" like "MeanF0=X"
          # This value is not accepted by Grew, so it is replaced by "MeanF0_X=Yes"
          syl_misc = syl_misc.replace("MeanF0=X", "MeanF0_X=Yes")
          syl_misc = syl_misc.replace("Duration=X", "Duration_X=Yes")
          syl_misc = syl_misc.replace("MaxAmplitude=X", "MaxAmplitude_X=Yes")
          syl_misc = syl_misc.replace("AvgAmplitude=X", "AvgAmplitude_X=Yes")
          if syl_misc == "":
            syl_misc = "_"
          syl_id = f"{fields[0]}.{syl_number}"
          syl_form = syl_feats.get(prefix, "__undef__")
          if syl_form == "":
            syl_form = "__empty__"
          f.write(f"{syl_id}\t_\t_\t_\t_\tSylForm={syl_form}\t{fields[0]}\tSyl={syl_number}\t_\t{syl_misc}\n")
          syl_number += 1
