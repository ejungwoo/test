void draw_all()
{
    const char *fileNames[] = {
        "file0.root",
        "file1.root",
        "file2.root",
        "file3.root",
    };

    const char *legendTitles[] = {
        "file0",
        "file1",
        "file2",
        "file3",
    };

    auto cvs = new TCanvas();
    auto hist = new TH2D("hist_graph03","",100,0,1000,100,0,0.1);
    hist -> SetStats(0);
    hist -> Draw();
    auto legend = new TLegend(0.6,1,0.6,1);
    for (auto iGas=0; iGas<4; ++iGas) {
        auto file = new TFile(fileNames[iGas]);
        auto graph = file -> Get<TGraph>("graph03");
        graph -> SetMarkerColor(iGas);
        graph -> Draw("same");
        legend -> AddEntry(graph,fileNames[iGas],"pl");
    }
    legend -> Draw();
}
