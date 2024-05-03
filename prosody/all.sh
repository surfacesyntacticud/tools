indir=SUD_Naija-NSC
outdir=SUD_Naija-NSC-prosody
pattern=*_MG.conllu  # _MG to have only monologues (dialogue are not annotated at the syllables level)

for infile in ${indir}/${pattern}
do
  outfile=`echo $infile | sed "s+${indir}+${outdir}+"`
  echo "$infile --> $outfile"
  python3 make_syllables.py $infile | grew transform -config sud -grs fused.grs -o $outfile
done
