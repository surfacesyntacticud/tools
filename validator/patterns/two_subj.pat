%VALIDATOR%Two <code>subj</code> relations cannot appear with the same governor
pattern {
  N -[subj]-> S1;
  N -[subj]-> S2;
  id(S1) < id(S2);  % avoid duplicate solutions
}
