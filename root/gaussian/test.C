void test()
{
    gRandom -> SetSeed(time(0));
    auto f1 = new TF1("f1","gaus(0)",-20,20);
    f1 -> SetParameters(10,0,4);
    auto hist = new TH1D("hist","",40,-20,20);
    for (auto i=0; i<10000; ++i)
        hist -> Fill(f1->GetRandom());
    ofstream file("data.csv");
    for (auto bin=1; bin<=40; ++bin)
        file << hist -> GetBinCenter(bin) << ", " << hist -> GetBinContent(bin) << endl;

    THttpServer* serv = new THttpServer("http:8080");
    TCanvas *cvs = new TCanvas("C","canvas");
    serv -> Register("/", cvs);
    cvs -> cd();
    hist -> Draw();
}
