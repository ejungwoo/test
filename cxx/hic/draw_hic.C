#include "TMath.h"

class ecircle
{
  public:
    ecircle(Double_t x, Double_t y, Double_t r, Double_t r2=0) { fX = x; fY = y; fR = r; fR2 = r2; }
    TGraph *DrawCircle(Int_t nPoints = 100, Double_t theta1 = 0, Double_t theta2 = 0) {
      if (theta1==theta2 && theta1==0) theta2 = 2*TMath::Pi();
      auto graph = new TGraph();
      TVector3 center(fX,fY,0);
      for (auto iPoint=0; iPoint<=nPoints; ++iPoint) {
        TVector3 pointer(fR,0,0);
        pointer.RotateZ(iPoint*(theta2-theta1)/nPoints);
        auto point = center + pointer;
        graph -> SetPoint(graph->GetN(), point.X(), point.Y());
      }
      return graph;
    }
    TGraph *DrawExcited(Int_t nPoints = 100, Int_t nDiv = 15, Double_t theta1 = 0, Double_t theta2 = 0) {
      if (theta1==theta2 && theta1==0) theta2 = 2*TMath::Pi();
      auto graph = new TGraph();
      TVector3 center(fX,fY,0);
      for (auto iPoint=0; iPoint<=nPoints; ++iPoint) {
        int mod = iPoint%(nPoints/nDiv);
        double rr = 0.5*(fR2-fR)*TMath::Sin(double(mod)/(nPoints/nDiv)*2*TMath::Pi()) + 0.5*(fR+fR2);
        TVector3 pointer(rr,0,0);
        pointer.RotateZ(iPoint*(theta2-theta1)/nPoints);
        auto point = center + pointer;
        graph -> SetPoint(graph->GetN(), point.X(), point.Y());
      }
      return graph;
    }
    Double_t fX = 0;
    Double_t fY = 0;
    Double_t fR = 0;
    Double_t fR2 = 0;
};

void draw_hic()
{
  bool dodebug = false;
  bool printexc = false;
  int printpid = -1;

  int colorProton = kBlue-10;

  //int seed = time(0);
  int seed = 1653487538;
  //int seed = 1653485343;
  cout << seed << endl;
  gRandom = new TRandom3();
  gRandom -> SetSeed(seed);

  auto draw_step = [colorProton,dodebug,printpid,printexc](int istep, TVirtualPad *cvs, TH2D *hist)
  {
    const int numspc = 9;
    TString ptitle[numspc]    = {"n","p","d","t","3","4","6He","6Li","7Li"};
    int     scp_ratio[numspc] = { 23, 20, 15, 10, 10, 15,    4,    3,    3};
    int     scp_pnnum[numspc] = {  1,  1,  2,  3,  3,  4,    6,    6,    7};
    int     scp_pnum[numspc]  = {  0,  1,  1,  1,  2,  2,    2,    3,    3};
    int     scp_nnum[numspc]  = {  1,  0,  1,  2,  1,  2,    4,    3,    4};
    int countpn = 0;
    for (auto icount=0; icount<numspc; icount++)
      countpn += scp_ratio[icount]*scp_pnnum[icount];

    auto rnuc1 = 2.;
    auto rnuc2 = 3.;
    auto cent1 = -28.;
    auto cent2 = +28.;
    auto rmax1 = 15.;
    auto rmax2 = 15.;
    auto numNucleons = 256;
    //auto numfg = 0;
    if (istep==2) {
      cent1 = -0.;
      cent2 = +0.;
      //rmax1 = 22.;
      //rmax2 = 22.;
      rmax1 = TMath::Power(2*rmax2*rmax2*rmax2,1./3);
      rmax2 = TMath::Power(2*rmax2*rmax2*rmax2,1./3);
    }
    if (istep==3) {
      rnuc1 = rnuc1-(rnuc2-rnuc1)*0.2;
      rnuc2 = rnuc2+(rnuc2-rnuc1)*0.2;
      rmax1 = 0.;
      auto rmaxa = TMath::Power(2*rmax2*rmax2*rmax2,1./3);
      rmax2 = TMath::Power(3*rmaxa*rmaxa*rmaxa,1./3);
    }
    if (istep==4) {
      rnuc1 = rnuc1-(rnuc2-rnuc1)*0.3;
      rnuc2 = rnuc2+(rnuc2-rnuc1)*0.3;
      rmax1 = 10.;
      rmax2 = 60.;
    }
    if (istep==5) {
      rnuc1 = rnuc1-(rnuc2-rnuc1)*0.4;
      rnuc2 = rnuc2+(rnuc2-rnuc1)*0.4;
      rmax1 = 20.;
      rmax2 = 100.;
      scp_ratio[0] = 34;
      scp_ratio[1] = 30;
      scp_ratio[2] = 18;
      scp_ratio[3] = 13;
      scp_ratio[4] = 10;
      scp_ratio[5] = 14;
      scp_ratio[6] = 2;
      scp_ratio[7] = 2;
      scp_ratio[8] = 1;
    }

    if (dodebug||printexc)
      draw(hist,cvs);
    else {
      cvs -> SetFrameLineColor(0);
      draw(hist,cvs,"a");
    }

    if (istep==1||istep==2)
    {
      TF1 *ff0 = new TF1("f1Random0","1+1./[0]*x",0,rmax1); ff0 -> SetParameter(0,rmax1);
      TF1 *ff1 = new TF1("f1Random1","1+1./[0]*x",0,rmax2); ff1 -> SetParameter(0,rmax2);
      for (auto i=0; i<numNucleons; ++i) {
        double cent, rmax;
        if (i%2==0) cent = cent1;
        if (i%2==1) cent = cent2;
        if (i%2==0) rmax = rmax1;
        if (i%2==1) rmax = rmax2;
        double rnuc = rnuc1+(rnuc2-rnuc1)*2*int(i/2)/numNucleons;

        double r0;
        if (istep==1)
          r0 = gRandom -> Uniform(0,rmax);
        else if (istep==2) {
          if (i%2==0) r0 = ff0 -> GetRandom();
      return;
          if (i%2==1) r0 = ff1 -> GetRandom();
        }
        auto phi = gRandom -> Gaus(0,2*TMath::Pi());
        TVector3 pos(r0,0,0);
        pos.SetPhi(phi);
        pos.SetX(pos.x()+cent);

        auto graph = ecircle(pos.x(),pos.y(),rnuc).DrawCircle();
        if (i%4==0||i%4==1) graph -> SetFillColor(colorProton);
        if (i%4==2||i%4==3) graph -> SetFillColor(kWhite);
        graph -> Draw("samefl");
      }
      
      if (istep==2) {
        auto graph_volume = ecircle(cent1,0,rmax2*1.23).DrawCircle();
        graph_volume -> SetLineStyle(2);
        graph_volume -> Draw("samel");

        auto tt = new TLatex(0,-rmax2-15,"V_{0}");
        tt -> SetTextFont(133);
        tt -> SetTextSize(30);
        tt -> SetTextAlign(22);
        tt -> Draw();
      }
    }
    else {
      int numr = 0;
      for (auto icount=0; icount<numspc; icount++)
        numr += scp_ratio[icount];
      double rmin = rmax1;
      double rmax = rmax2;
      TF1 *f1Random[2];
      f1Random[0] = new TF1("f1Random","1+2./[0]*x",0,rmax);
      f1Random[0] -> SetParameter(0,rmax);
      f1Random[1] = new TF1("f1Random1","(x<[1])*0+(x>=[1])*(1+1./[0]*(x-[1]))",0,rmax2);
      f1Random[1] -> SetParameter(0,rmax2);
      f1Random[1] -> SetParameter(1,rmax1);

      int count_nucleons = 0;
      for (auto i100=0; i100<numr; i100++)
      {
        int ipid = gRandom -> Integer(numspc);
        if (scp_ratio[ipid]==0) {
          i100--;
          continue;
        }
        //if (dodebug) cout << ipid << " " << scp_ratio[ipid] << endl;
        double rc;
        if (istep==3) 
          rc = f1Random[0] -> GetRandom();
        else if (istep==2)
          rc = f1Random[1] -> GetRandom();
        else
          rc = gRandom -> Uniform(rmin,rmax);
        auto phic = gRandom -> Gaus(0,2*TMath::Pi());
        TVector3 posc(rc,0,0);
        posc.SetPhi(phic);

        scp_ratio[ipid] = scp_ratio[ipid]-1;
        int npnum = scp_pnnum[ipid];
        int pnum = scp_pnum[ipid];
        int nnum = scp_nnum[ipid];

        double rnuc = rnuc1+(rnuc2-rnuc1)*i100/numr;
        double rcluster = rnuc * 1.5;

        if (ipid==printpid) cout << setw(5) << i100 << " ipid=" << ptitle[ipid] << "(" << nnum << "," << pnum << ")";

        bool sqdecay = false;
        if (istep==4&&ipid>2) {
          int isq = 1;
          if (ipid>5)
            isq = gRandom -> Integer(3);
          else
            isq = gRandom -> Integer(5);
          if (isq==0||isq==1) sqdecay = true;
        }

        for (auto inuc=0; inuc<npnum; inuc++)
        {
          int inp = gRandom -> Integer(2);
          if (ipid==3) {
            if (inuc==0) inp = 0;
            if (inuc==1) inp = 1;
            if (inuc==2) inp = 0;
          }
          else if (ipid==4) {
            if (inuc==0) inp = 1;
            if (inuc==1) inp = 0;
            if (inuc==2) inp = 1;
          }
          else if (ipid==5) {
            if (inuc==0) inp = 0;
            if (inuc==1) inp = 1;
            if (inuc==2) inp = 0;
            if (inuc==3) inp = 1;
          }
          else if (ipid==6) {
            if (inuc==0) inp = 0;
            if (inuc==1) inp = 1;
            if (inuc==2) inp = 0;
            if (inuc==3) inp = 0;
            if (inuc==4) inp = 1;
            if (inuc==5) inp = 0;
          }
          else if (ipid==7) {
            if (inuc==0) inp = 0;
            if (inuc==1) inp = 1;
            if (inuc==2) inp = 0;
            if (inuc==3) inp = 1;
            if (inuc==4) inp = 0;
            if (inuc==5) inp = 1;
          }
          else if (ipid==8) {
            if (inuc==0) inp = 0;
            if (inuc==1) inp = 1;
            if (inuc==2) inp = 0;
            if (inuc==3) inp = 1;
            if (inuc==4) inp = 0;
            if (inuc==5) inp = 1;
            if (inuc==6) inp = 0;
          }
          else {
            if (inp==0) { if (nnum==0) { inuc--; continue; } else nnum += -1; }
            if (inp==1) { if (pnum==0) { inuc--; continue; } else pnum += -1; }
          }

          if (ipid==printpid) cout << " >" << inp << " ";

          double rn;
          if (sqdecay)
            rn = gRandom -> Uniform(0.4*rnuc,0.7*rnuc);
          else
            rn = gRandom -> Uniform(0.3*rnuc,0.5*rnuc);
          //auto rn = 0.5*rnuc;
          double phin = 0;
          if (npnum==1) rn = 0;
          //else if (npnum>1) phin = double(inuc)/npnum*2*TMath::Pi();
          else if (npnum>1) phin = double(inuc)/npnum*4*TMath::Pi();
          TVector3 posn(rn,0,0);
          posn.SetPhi(phin);
          posn += posc;

          auto graph = ecircle(posn.x(),posn.y(),rnuc).DrawCircle();

          if (inp==0) graph -> SetFillColor(kWhite);
          if (inp==1) graph -> SetFillColor(colorProton);
          graph -> Draw("samefl");

          auto tt = new TText(posc.x(),posc.y(),Form("%s",ptitle[ipid].Data()));
          tt -> SetTextFont(133);
          tt -> SetTextSize(20);
          tt -> SetTextAlign(22);
          if (dodebug)
            tt -> Draw();

          count_nucleons++;
        }
        if (ipid==printpid) cout << endl;

        if (sqdecay) {
          auto graph_sq = ecircle(posc.x(),posc.y(),1.9*rnuc,2.1*rnuc).DrawExcited();
          graph_sq -> SetLineColor(kPink);
          if (printexc)
            cout << setw(5) << i100 << " ipid=" << ptitle[ipid] << " " << posc.x() << " " << posc.y() << endl;
          graph_sq -> Draw("samel");
        }
      }

      if (istep==3) {
        auto graph_volume = ecircle(0,0,rmax2*1.2).DrawCircle();
        graph_volume -> SetLineStyle(2);
        graph_volume -> Draw("samel");

        auto tt = new TLatex(0,-rmax2-15,"( 1 + #chi ) #times V_{0}");
        tt -> SetTextFont(133);
        tt -> SetTextSize(30);
        tt -> SetTextAlign(22);
        tt -> Draw();
      }
      
      if (istep>=4) {
        cout << countpn << " " << count_nucleons << endl;
      }
    }
  };

  TCanvas *cvsAll;
  if (dodebug||printexc) {
    cvsAll = canvas("figure_hic",4,1,"single_sq");
    draw_step(2,cvsAll->cd(1),new TH2D("hist2","Source",100,-70,70,100,-70,70));
    draw_step(3,cvsAll->cd(2),new TH2D("hist3","Breakup",100,-70,70,100,-70,70));
    draw_step(4,cvsAll->cd(3),new TH2D("hist4","Sequential decay",100,-70,70,100,-70,70));
    draw_step(5,cvsAll->cd(4),new TH2D("hist5","Final state",100,-120,120,100,-120,120));
  }
  else if (1) {
    cvsAll = canvas("figure_hic",3,1,"hic");
    draw_step(2,cvsAll->cd(1),new TH2D("hist3","",100,-70,70,100,-70,70));
    //draw_step(4,cvsAll->cd(2),new TH2D("hist4","Sequential decay",100,-70,70,100,-70,70));
    //draw_step(5,cvsAll->cd(3),new TH2D("hist5","Final state",100,-120,120,100,-120,120));
  }
  else {
    cvsAll = canvas("figure_hic",4,1,"hic");
    //draw_step(1,cvsAll->cd(1),new TH2D("hist1","Before collision",100,-70,70,100,-70,70));
    draw_step(2,cvsAll->cd(1),new TH2D("hist2","Source",100,-70,70,100,-70,70));
    draw_step(3,cvsAll->cd(2),new TH2D("hist3","Breakup",100,-70,70,100,-70,70));
    draw_step(4,cvsAll->cd(3),new TH2D("hist4","Sequential decay",100,-70,70,100,-70,70));
    draw_step(5,cvsAll->cd(4),new TH2D("hist5","Final state",100,-120,120,100,-120,120));
  }

  //saveAll();
  //savePNG();
}

