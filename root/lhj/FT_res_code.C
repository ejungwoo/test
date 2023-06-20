#include <math.h>

void FT_res()
{
    /// @load mc file
    TFile *MCfilename = new TFile("../../macros_tpc/out_g4event_LH.mc.root", "READ");
    TTree *MCfiletree = (TTree *)MCfilename->Get("event");

    /// @declaration histogram
    TCanvas *c1 = new TCanvas("c1", "c1", 800, 600);
    gPad->SetGrid();
    // gStyle->SetOptStat(0);
    TH1D *Hist[4];
    TLegend *legend_data = new TLegend(0.719298, 0.744348, 0.943609, 0.918261, NULL, "brNDC");

    /// @MC Part
    TClonesArray *fMCTrack = new TClonesArray("KBMCTrack");
    TClonesArray *fMCStep40 = new TClonesArray("KBMCStep");
    TBranch *bMCTrack = (TBranch *)MCfiletree->GetBranch("MCTrack");
    TBranch *bMCStep40 = (TBranch *)MCfiletree->GetBranch("MCStep40");
    int num_MCfiletree = MCfiletree->GetEntriesFast();

    TVector3 MCMomentum_arr[num_MCfiletree];
    bMCTrack->SetAddress(&fMCTrack);
    bMCStep40->SetAddress(&fMCStep40);

    for (int iMCTree = 0; iMCTree < num_MCfiletree; iMCTree++)
    {
        MCfiletree->GetEntry(iMCTree);

        /// @MCTrack
        int num_MCTrack = fMCTrack->GetEntriesFast();
        double MCTrack_px[num_MCfiletree];
        double MCTrack_py[num_MCfiletree];
        double MCTrack_pz[num_MCfiletree];

        for (int iTrack = 0; iTrack < num_MCTrack; iTrack++)
        {
            auto MCTrack = (KBMCTrack *)fMCTrack->At(iTrack);
            if (MCTrack->GetCreatorProcessID() == 0) // primary particle
            {
                auto MCMomentum = MCTrack->GetMomentum();
                MCMomentum_arr[iMCTree] = MCMomentum.Unit();
            }
        }
    }

    /// @load result file
    TFile *KBfilename[4];
    TTree *KBfiletree[4];
    for (int i = 3; i < 4; i++)
    {
        Hist[i] = new TH1D(Form("hist_%i", i), Form("hist_%i", i), 500, 0, 30);

        KBfilename[i] = new TFile("../../../data/out_g4event_LH.conv.eb7a905.root", "READ");
        KBfiletree[i] = (TTree *)KBfilename[i]->Get("event");

        int num_KBfiletree = KBfiletree[i]->GetEntriesFast();

        TClonesArray *fKBTrack = new TClonesArray("KBHelixTrack");
        TClonesArray *fFTHit = new TClonesArray("FTHit");

        TBranch *bKBTrack = (TBranch *)KBfiletree[i]->GetBranch("Tracklet");
        TBranch *bFTHit = (TBranch *)KBfiletree[i]->GetBranch("FTHit");

        bKBTrack->SetAddress(&fKBTrack);
        bFTHit->SetAddress(&fFTHit);

        TVector3 KBMomentum_arr[num_KBfiletree];

        for (int iKBTree = 0; iKBTree < num_KBfiletree; iKBTree++)
        {
            KBfiletree[i]->GetEntry(iKBTree);

            /// @KBTrack
            int num_KBTrack = fKBTrack->GetEntriesFast();

            double KBTrack_px[num_KBfiletree];
            double KBTrack_py[num_KBfiletree];
            double KBTrack_pz[num_KBfiletree];

            for (int iKBTrack = 0; iKBTrack < num_KBTrack; iKBTrack++)
            {
                auto KBTrack = (KBHelixTrack *)fKBTrack->At(iKBTrack);
                auto KBMomentum = KBTrack->Momentum();

                KBTrack_px[iKBTree] = -KBMomentum.X();
                KBTrack_py[iKBTree] = -KBMomentum.Y();
                KBTrack_pz[iKBTree] = -KBMomentum.Z();
                // KBMomentum_arr[iKBTree] = KBMomentum.Unit();
                // KBMomentum_arr[iKBTree].SetXYZ(KBTrack_px[iKBTree], KBTrack_py[iKBTree], KBTrack_pz[iKBTree]);
                KBMomentum_arr[iKBTree] = {KBTrack_px[iKBTree], KBTrack_py[iKBTree], KBTrack_pz[iKBTree]};

                KBMomentum_arr[iKBTree] = KBMomentum_arr[iKBTree].Unit();
                // std::cout << KBMomentum _arr[iKBTree][2] << std::endl;
            }

            double dot_result = MCMomentum_arr[iKBTree].Dot(KBMomentum_arr[iKBTree]);
            double theta = acos(dot_result) * 180 / TMath::Pi();
            Hist[i]->Fill(theta);
        }

        /// @ dot product histogram fill
        Hist[i]->GetXaxis()->SetTitle("#theta");
        Hist[i]->GetYaxis()->SetTitle("count");
        Hist[i]->SetTitle(" ");
        Hist[i]->SetLineColor(i + 1);
        Hist[i]->Draw("same");
        legend_data->AddEntry(Form("hist_%i", i), Form("Layer amount %i", 2 * (i + 2)), "l");
    }
    legend_data->SetBorderSize(1);
    legend_data->SetTextAlign(22);
    legend_data->SetTextFont(62);
    legend_data->SetTextSize(0.0313043);
    legend_data->SetTextAlign(12);
}
