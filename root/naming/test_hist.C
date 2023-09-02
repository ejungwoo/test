void test_hist()
{
    cout << "histogram" << endl;
    new TH1D("name1","",10,0,10);
    auto directory1 = new TDirectory("directory1","recreate");
    directory1 -> cd();
    new TH1D("name1","",10,0,10);
}
