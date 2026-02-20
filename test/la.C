void la()
{
    TCanvas *cvs = new TCanvas();
    auto graph = new TGraph();
    graph -> SetPoint(0,1,2);
    graph -> SetPoint(1,2,3);
    graph -> Draw("al");
    auto graph2 = (TGraph*) graph -> Clone();
    graph2 -> Draw("same*");
    delete graph;
    //cvs -> Remove(graph);
}
