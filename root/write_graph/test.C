void test() {
    auto file = new TFile("file3.root","recreate");
    auto graph = new TGraph();
    int iType = 0;
    int iProperty = 0;
    graph -> SetName(Form("graph%d%d",iType,iProperty));
    graph -> Write();
}
