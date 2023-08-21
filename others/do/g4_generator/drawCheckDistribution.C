void drawCheckDistribution()
{
    TString dummyC;
    int     dummyI;
    int     eventID;
    double  dummyD;

    int     numParticles;
    int     pdg;
    int     ip;
    double  px;
    double  py;
    double  pz;
    double  phi_deg;
    double  theta_deg;

    auto file = new TFile("summary.root","recreate");
    auto tree = new TTree("particle","");
    tree -> Branch("ip"   ,&ip);
    tree -> Branch("px"   ,&px);
    tree -> Branch("py"   ,&py);
    tree -> Branch("pz"   ,&pz);
    tree -> Branch("phi"  ,&phi_deg);
    tree -> Branch("theta",&theta_deg);

    int numEvents;

    ifstream file_gen("two_proton.gen");
    file_gen >> dummyC;
    file_gen >> numEvents;
    for (auto iEvent=0; iEvent<numEvents; ++iEvent)
    {
        file_gen >> eventID >> numParticles >> dummyD >> dummyD >> dummyD;

        for (ip=0; ip<numParticles; ++ip)
        {
            file_gen >> pdg >> px >> py >> pz;
            TVector3 mom(px,py,pz);
            theta_deg = mom.Theta()*TMath::RadToDeg();
            phi_deg = mom.Phi()*TMath::RadToDeg();
            tree -> Fill();
        }
    }

    auto cvs = new TCanvas("cvs","",1200,700);
    cvs -> Divide(2,2);
    cvs -> cd(1); tree -> Draw("theta>>theta0(180,0,180)","ip==0");
    cvs -> cd(2); tree -> Draw("theta>>theta1(180,0,180)","ip==1");
    cvs -> cd(3); tree -> Draw("phi>>phi0(360,0,360)","ip==0");
    cvs -> cd(4); tree -> Draw("phi>>phi1(360,0,360)","ip==1");

    file -> cd();
    tree -> Write();
}
