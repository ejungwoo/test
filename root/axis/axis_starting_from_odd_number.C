void axis_starting_from_odd_number() // 
{
    int n = 20;
    auto hist = new TH2D("hist","",n,60,80,100,0,10);
    hist -> SetNdivisions(n);
    auto axis = hist -> GetXaxis();
    axis -> SetTickSize(0);
    for (auto i=0; i<=n; i+=2)
        axis -> ChangeLabel(i+1,-1,-1,-1,-1,-1," ");
    hist -> Draw();
    for (auto i=1; i<n; i+=2)
        (new TLine(i+60,0,i+60,0.2)) -> Draw();
}
