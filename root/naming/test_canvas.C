void test_canvas()
{
    cout << "canvas" << endl;
    new TCanvas("name1","");
    auto directory2 = new TDirectory("directory2","recreate");
    directory2 -> cd();
    new TCanvas("name1","");
}
