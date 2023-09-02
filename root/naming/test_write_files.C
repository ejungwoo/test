void test_write_files()
{
    auto file1 = new TFile("file1.root","recreate");
    auto cvs1 = new TCanvas("cvs1","");
    auto hist1 = new TH1D("hist1","hist1",100,0,100);
    hist1 -> Draw();
    cvs1 -> Write();

    auto file2 = new TFile("file2.root","recreate");
    auto cvs2 = new TCanvas("cvs1","");
    auto hist2 = new TH1D("hist2","hist2",100,0,100);
    hist2 -> Draw();
    cvs2 -> Write();
}
