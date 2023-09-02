void test_poisson() {
    auto f1 = new TF1("f1","TMath::Poisson(x,1)",-5,20);
    f1 -> SetNpx(500);
    f1 -> Draw();
}
