void number_check()
{
  TString a = "-123+f2.14";
  if (a[0]=='-') cout << a << endl;
  //cout << a.IsFloat() << endl;
  //cout << a.IsDigit() << endl;
  //cout << TFormula("f",a).Eval(0) << endl;
  cout << TFormula("f",a).IsValid() << endl;
}
