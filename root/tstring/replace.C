void replace()
{
  TString line = "name {value} e{env} ?????";
  auto i1 = line.Index("e{");
  auto i2 = line.Index("}");
  auto i3 = line.Index("}",1,i1,TString::kExact);
  cout << line << endl;
  cout << i1 << " " << i2 << " " << i3 << endl;
  cout << line(i1+2,i3-i1-2) << endl;
  line.Replace(i1,i3-i1+1,"!!!");
  cout << line << endl;
}
