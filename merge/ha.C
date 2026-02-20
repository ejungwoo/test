void ha()
{
    auto file = new TFile("file1.root","recreate");
    auto hist1 = new TH2D("hist1","",20,0,20,20,0,20);
    for (auto i=0; i<2000; ++i)
        hist1 -> Fill(gRandom->Gaus(5,2),gRandom->Gaus(7,2));
    hist1 -> Write();

    auto hist2 = new TH2D("hist2","",20,0,20,20,0,20);
    for (auto i=0; i<2000; ++i)
        hist2 -> Fill(gRandom->Gaus(15,2),gRandom->Gaus(9,2));
    hist2 -> Write();

    int bin10 = hist1 -> GetXaxis() -> FindBin(10);
    int nbinsx = hist1 -> GetXaxis() -> GetNbins();
    int nbinsy = hist1 -> GetYaxis() -> GetNbins();
    for (auto binx=bin10; binx<=nbinsx; ++binx)
        for (auto biny=1; biny<=nbinsy; ++biny)
        {
            hist1 -> SetBinContent(binx,biny,0);
            auto content = hist2 -> GetBinContent(binx,biny);
            hist1 -> SetBinContent(binx,biny,content);
        }

    auto cvs = new TCanvas("cvs","",2000,1000);
    cvs -> Divide(2,1);
    cvs -> cd(1); hist1 -> Draw();
    cvs -> cd(2); hist2 -> Draw();
}
