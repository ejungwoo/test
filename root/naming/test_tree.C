void test_tree()
{
    auto dir = new TDirectory();
    dir -> cd();
    auto hist = new TH1D("hist","",100,0,10);

    auto file = new TFile("file.root","recreate");
    auto tree = new TTree("event","");
    double a, b;
    tree -> Branch("a",&a);
    tree -> Branch("b",&b);
    for (auto i=0; i<1000; ++i) {
        a = gRandom -> Uniform();
        b = gRandom -> Uniform();
        tree -> Fill();
    }
    tree -> Draw("a>>hist");
}
