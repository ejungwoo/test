void ss_remove_replace()
{
  //std::string line = "name    this is e{ROOTSYS} and e{ROOTSYS} e{ROOTSYS} e{asdf}# asd1fas2df asdfasdf";
  std::string line = "name    value value2    # !";
  stringstream ss(line);
  TString parName;
  ss >> parName;
  TString parValues = line;
  parValues.Remove(0,parName.Sizeof()-1);
  while (parValues[0]==' ') {
    parValues.Remove(0,1);
  }

  int icomment = parValues.Index("#");
  TString parComment = parValues(icomment,parValues.Sizeof());
  parValues = parValues(0,icomment);
  while (parValues[parValues.Sizeof()-2]==' ') {
    parValues.Remove(parValues.Sizeof()-2,1);
  }

  cout << parName << endl;
  cout << parValues << " " << parValues.Sizeof() << endl;
  cout << parComment << endl;

  parValues.Tokenize(" ") -> Print("all*");

  //cout << ss <<endl;
  //int i = ss.Index("e{",2);
  //while (i>=0) {
  //  int f = ss.Index("}");
  //  cout << i << " " << f << endl;
  //  ss.Replace(i,f-i+1,"rootsys");
  //  cout << ss << endl;
  //  i = ss.Index("e{",2);
  //}
}
