void draw()
{
    TString name[] = {"f1","f2","f3"};
    double v1, v2, v3, v4;
    TGraph *graph[4] = {0};
    for (auto i : {0,1,2}) {
        graph[i] = new TGraph();
        auto g = graph[i];
        TString fileName = name[i] + ".txt";
        ifstream file(fileName);
        while (file>>v1>>v2>>v3>>v4)
        {
            g -> SetPoint(g->GetN(),g->GetN(),v1);
            g -> SetPoint(g->GetN(),g->GetN(),v2);
            g -> SetPoint(g->GetN(),g->GetN(),v3);
            g -> SetPoint(g->GetN(),g->GetN(),v4);
        }
    }
    //auto hist = new TH2D("hist","",100,0,300,100,0.00001,1.0E+20);
    auto hist = new TH2D("hist","",100,0,300,100,-1.0E+10,1.0E+10);
    auto cvs = new TCanvas("cvs","",3000,2000);
    //cvs -> SetLogy();
    graph[0] -> SetLineColor(kBlack);
    graph[1] -> SetLineColor(kBlue);
    graph[2] -> SetLineColor(kRed);
    auto draw = top -> CreateDrawing();
    draw -> Add(hist);
    draw -> Add(graph[0]);
    draw -> Add(graph[1]);
    draw -> Add(graph[2]);
    top -> CreateDrawing() -> Add(graph[0]);
    top -> CreateDrawing() -> Add(graph[1]);
    top -> CreateDrawing() -> Add(graph[2]);
}
