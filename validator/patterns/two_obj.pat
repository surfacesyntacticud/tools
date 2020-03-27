%VALIDATOR%Two <code>comp:obj</code> relations cannot appear with the same governor
pattern {
  N -[comp:obj]-> S1;
  N -[comp:obj]-> S2;
  id(S1) < id(S2);  % avoid duplicate solutions
}
