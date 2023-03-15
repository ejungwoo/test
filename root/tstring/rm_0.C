void rm_0() {
  //TString a = "1231.000000";
  //TString a = "1231.0000";
  //TString a = ".12310000";
  //TString a = "12310000";
  TString a = "123.10000";

  while (a.Index(".")>=0 && a.EndsWith("0") && a.Index(".")<a.Sizeof()-2) {
    cout << a << endl;
    a.Remove(a.Sizeof()-2,1);
  }
  cout << a << endl;
  if (a.EndsWith("."))
    a.Remove(a.Sizeof()-2,1);
  cout << a << endl;
}
