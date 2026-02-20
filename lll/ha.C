void ha()
{
    new TCanvas("c1", "", 1500, 1500);
    auto img = TImage::Open("example.png");
    img->Draw();
}
