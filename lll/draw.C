void DrawGraph(vector<vector<double>> values, int lineColor, int lineWidth);
void draw()
{
    gStyle -> SetOptStat(0);

    double values[][2] = {
        {0.150367, 0.755508}, {0.150367, 0.501271}, {0.273031, 0.502119}, {0.271362, 0.554661}, {0.212116, 0.552119}, {0.208778, 0.758051},
        {0.287216, 0.752119}, {0.295561, 0.504661}, {0.358144, 0.502119}, {0.356475, 0.752119},

        {0.394025, 0.752119}, {0.392356, 0.503814}, {0.510013, 0.502966}, {0.510848, 0.555508}, {0.449099, 0.551271}, {0.444092, 0.752966}, 

        {0.583445, 0.750424}, {0.526702, 0.502966}, {0.577603, 0.501271}, {0.587617, 0.550424}, {0.646862, 0.550424}, {0.655207, 0.502966}, {0.706943, 0.502966}, {0.652704, 0.753814},

        {0.615154, 0.67839 },
        {0.598465, 0.594492},
        {0.641856, 0.594492},
        {0.735314, 0.755508},
        {0.731142, 0.497881},
        {0.785381, 0.498729},
        {0.784546, 0.558051},
        {0.803738, 0.587712},
        {0.845461, 0.496186},
        {0.898865, 0.498729},
        {0.840454, 0.642797},
        {0.906375, 0.752966},
        {0.843792, 0.752966},
        {0.785381, 0.655508},
        {0.784546, 0.760593},
    };


    new TCanvas("cvs","",1500,1500);
    auto hist = new TH2D("hist","",100,0,1,100,0,1);
    hist -> Draw();

    auto graph = new TGraph();
    for (double *value : values)
        graph -> SetPoint(graph->GetN(),value[0],value[1]);
    graph -> Draw("l");

    //////////////////////////////////////////////////////

    double thick1 = 0.058411;
    double height1 = 0.254237;
    double width1 = 0.122792;
    double thick12 = 0.053370;
    double x1 = 0.15;
    double y1 = 0.5;

    vector<vector<double>> values1 = { {x1,y1}, {x1+width1,y1}, {x1+width1,y1+thick12}, {x1+thick1,y1+thick12}, {x1+thick1,y1+height1}, {x1,y1+height1}, {x1,y1}, };
    DrawGraph(values1, kRed, 2);

    double dx2 = 0.145;
    double x2 = x1 + dx2;
    double y2 = y1;
    double height2 = height1;
    double width2 = thick1;

    vector<vector<double>> values2 = { {x2,y2}, {x2+width2,y2}, {x2+width2,y2+height2}, {x2,y2+height2}, {x2,y2}, };
    DrawGraph(values2, kRed, 2);

    double dx3 = 0.240;
    double thick3 = thick1;
    double height3 = height1;
    double width3 = width1;
    double thick32 = thick12;
    double x3 = x1 + dx3;
    double y3 = y1;

    vector<vector<double>> values3 = { {x3,y3}, {x3+width3,y3}, {x3+width3,y3+thick32}, {x3+thick3,y3+thick32}, {x3+thick3,y3+height3}, {x3,y3+height3}, {x3,y3}, };
    DrawGraph(values3, kRed, 2);

    double dx4 = 0.375;
    double width4 = 0.185;
    double thick4 = thick12;
    double x4 = x1 + dx4;
    double y4 = y1;

    vector<vector<double>> values4 = { {x4,y4}, {x4+width4,y4}};
    DrawGraph(values4, kRed, 2);
    //vector<vector<double>> values4 = { {0.526702, 0.502966}, {0.577603, 0.501271}, {0.587617, 0.550424}, {0.646862, 0.550424}, {0.655207, 0.502966}, {0.706943, 0.502966}, {0.652704, 0.753814}, {0.583445, 0.750424}, };
    //DrawGraph(values4, kRed, 2);
        

    //{0.287216, 0.752119}, {0.295561, 0.504661}, {0.358144, 0.502119}, {0.356475, 0.752119},

}
void DrawGraph(vector<vector<double>> values, int lineColor, int lineWidth)
{
    auto graph = new TGraph();
    for (vector<double> value : values)
        graph -> SetPoint(graph->GetN(),value[0],value[1]);
    graph -> SetLineColor(kRed);
    graph -> SetLineWidth(2);
    graph -> Draw("samel");
}

