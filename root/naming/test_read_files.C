void test_read_files()
{
    auto file1 = new TFile("file1.root","read");
    auto cvs1 = file1 -> Get<TCanvas>("cvs1");
    cvs1 -> SetName("cvsasdfasdf");
    cvs1 -> Draw();

    auto file2 = new TFile("file2.root","read");
    auto cvs2 = file2 -> Get<TCanvas>("cvs1");
    cvs2 -> Draw();
}
