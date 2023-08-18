void test()
{
    std::map<TString, TObject*> objects;
    objects["jw"] = new TNamed("jw","lee");
    cout << objects["jw"] << endl;
    cout << objects["je"] << endl;
    cout << objects.at("je") << endl;
    cout << (objects["je"]==nullptr) << endl;
    cout << (objects.at("je")==nullptr) << endl;
}
