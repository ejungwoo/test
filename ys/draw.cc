double adc_mean1[32]={18263.9,19539.2,19043.8,19114.7,19582.7,18333.5,19654.8,19694.9,18915.8,19013.4,18889.8,18738.8,19391.6,18800.9,19093.2,19197.2,20322.2,20245.1,19673.2,19785.5,20140.1,20532.6,20584.8,20844.9,20444.7,20078.4,20281.6,20192.4,19839.4,20395.1,19872.9,20220};
double adc_mean2[32]={19528.1,19579,12265.8,19104.7,19562.2,18337.9,19569.7,19689.5,18937,18981.5,18824.7,18968.3,19373.6,18798.7,19098.6,19118,20358.6,20278.7,19706.4,19812.9,20176.3,20564.8,20620.9,20870.4,20463.7,20100.5,20287.5,20189,19863.9,20429.3,19891.9,20254.3};

void draw()
{
    gStyle -> SetOptStat(0);

    TFile *file = new TFile("data.root","read");
    TTree *tree = (TTree *)file -> Get("Data");
    double numEvents = tree -> GetEntries();

    UShort_t Channel;
    ULong64_t Timestamp;
    UShort_t Energy;

    tree -> SetBranchAddress("Channel",&Channel);
    tree -> SetBranchAddress("Timestamp",&Timestamp);
    tree -> SetBranchAddress("Energy",&Energy);

    // all
    TH1D *hista_ch = new TH1D("hista_ch","hista_ch",32,0,32);
    TH1D *hista_dt = new TH1D("hista_dt","hista_dt",5,0,8000*5);
    TH1D *hista_di = new TH1D("hista_di","hista_di",10,0,10);

    // correlated
    TH2D *histc_hit = new TH2D("histc_hit","histc_hit",16,0,16,16,16,32);
    TH2D *histc_chhit = new TH2D("histc_chhit","histc_chhit",1,0,16,16,16,32);
    TH1D *histc_energy = new TH1D("histc_energy","histc_energy",100,0,8000);
    TH2D *histc_energy2 = new TH2D("histc_energy2","histc_energy2",100,5000,6000,100,5000,6000);
    TH1D *histc_dt = new TH1D("histc_dt","histc_dt",5,0,8000*5);
    TH1D *histc_ch = new TH1D("histc_ch","histc_ch",32,0,32);
    TH2D *histc_chdt = new TH2D("histc_chdt",";channelID;#Delta Timestamp",32,0,32,5,0,8000*5);

    double cal_value[32];
    TH1D *hist_cal[32];
    for(int i=0 ; i<32 ; ++i) {
        cal_value[i]=5486/adc_mean2[i];
        hist_cal[i] = new TH1D(Form("hist_cal_%d",i),"",100,5200,5600);
    }

    const int numCompare = 100;
    ULong64_t aTimeStamp[numCompare] = {0};
    UShort_t aChannel[numCompare] = {0};
    UShort_t aEnergy[numCompare] = {0};
    int aEventID[numCompare] = {0};

    cout<<numEvents<<endl;

    //numEvents = 5;
    for(int eventID=0;eventID<numEvents;eventID++)
    {
        tree -> GetEntry(eventID);
        double currentEnergy = Energy*cal_value[Channel];

        hist_cal[Channel] -> Fill(currentEnergy);

        int lEvent = eventID%numCompare;
        aTimeStamp[lEvent] = Timestamp;
        aChannel[lEvent] = Channel;
        aEnergy[lEvent] = currentEnergy;
        aEventID[lEvent] = eventID;

        hista_ch -> Fill(Channel);

        for(int iEvent=0 ; iEvent<numCompare; iEvent++)
        {
            if(aChannel[iEvent]==Channel)
                continue;

            ULong64_t diffTime = fabs(Timestamp - aTimeStamp[iEvent]);
            hista_dt -> Fill(diffTime);

            int diffEventID = eventID - aEventID[iEvent];

            if(diffTime >= 0 && diffTime < 1e+5
                //&& diffEventID == 2
                && aEnergy[iEvent] > 5400
                && aEnergy[iEvent] < 5550
                && currentEnergy > 5400
                && currentEnergy < 5550
                )
            {
                if (Channel>15 && aChannel[iEvent]<=15)
                {
                    hista_di -> Fill(diffEventID);
                    histc_ch -> Fill(Channel);
                    histc_ch -> Fill(aChannel[iEvent]);
                    histc_chdt -> Fill(Channel,diffTime);
                    histc_chdt -> Fill(aChannel[iEvent],diffTime);
                    histc_hit -> Fill(aChannel[iEvent],Channel);
                    histc_chhit -> Fill(aChannel[iEvent],Channel);
                    histc_energy -> Fill(currentEnergy);
                    histc_energy2 -> Fill(currentEnergy,aEnergy[iEvent]);
                    histc_dt -> Fill(diffTime);
                    break;
                }
            }
        }
    }

    auto cvs_e = new TCanvas("cvse","cvse",3000,2000);
    cvs_e -> Divide(7,5);
    for (auto i=0; i<32; ++i) {
        cvs_e -> cd(i+1);
        hist_cal[i] -> Draw();
    }

    histc_hit -> SetMinimum(0);
    histc_dt -> SetMinimum(0);
    histc_ch -> SetMinimum(0);
    histc_chdt -> SetMinimum(0);
    histc_chhit -> SetMinimum(0);
    histc_energy -> SetMinimum(0);
    histc_energy2 -> SetMinimum(0);
    hista_ch -> SetMinimum(0);
    hista_dt -> SetMinimum(0);

    auto cvs = new TCanvas("cvs","cvs",3200,1500);
    cvs -> Divide(4,2);
    //cvs -> cd(1); histc_energy -> Draw();
    cvs -> cd(1); hista_di -> Draw();
    cvs -> cd(2); histc_energy2 -> Draw("colz");
    cvs -> cd(3); hista_ch -> Draw("colz");
    cvs -> cd(4); hista_dt -> Draw();
    cvs -> cd(5); histc_hit -> Draw("colz");
    cvs -> cd(6); histc_chhit -> Draw("colz");
    cvs -> cd(7); histc_dt -> Draw();
    //cvs -> cd(8); histc_ch -> Draw();
    cvs -> cd(8); histc_chdt -> Draw("colz");

    auto cvs1 = new TCanvas("cvs1","",800,600);
    cvs1 -> SetLeftMargin(0.15);
    histc_chdt -> Draw("colz");
}
