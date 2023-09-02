void hist_clear()
{
    auto hist = new TH1D("hist","",10,0,10);
    hist -> Fill(2);
    hist -> Fill(5);
    hist -> Fill(5);
    hist -> Fill(5);
    hist -> Fill(5);
    hist -> Draw();

    auto file1 = new TFile("file1.root","recreate");
    hist -> Write();

    hist -> Reset("ICES");
    hist -> Fill(1);
    hist -> Fill(1);
    hist -> Fill(4);
    hist -> Fill(4);
    hist -> Fill(8);
    hist -> Draw();

    auto file2 = new TFile("file2.root","recreate");
    hist -> Write();
}
