void replace()
{
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

    {
        TString line = " l || line#print out line comment";
        auto i1 = line.Index("#");
        cout << line(i1+1,line.Sizeof()) << endl;
        TString justnames = line(0,i1);
        cout << justnames << endl;
        auto list = justnames.Tokenize("||");
        TIter next(list);
        TObjString* obstring;
        while ((obstring=(TObjString*)next()))
        {
            TString tok = obstring -> GetString();
            tok = tok.Strip(TString::kBoth);
            tok.ReplaceAll(" ","_");
            cout << tok << endl;
            //TString token1 = ((TObjString *) array->At(1)) -> GetString();
        }
    }
}
