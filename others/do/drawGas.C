void drawTree(TTree *treeGas, TString gasName)
{
    TString nameType[2] = {"Drift", "GEM"}; // E-Field range in Drift area, and GEM hole area
    TString nameProperties[6] = {"Electric Field", "Drift Velocity", "Longitude Diffusion", "Transverse Diffusion", "Townsend Coefficient", "Attachment Coefficient"};
    TString titleProperties[6] = {"E [V/cm]", "V_{D} [cm/us]", "D_{L} [cm/#sqrt{cm}]", "D_{T} [cm/#sqrt{cm}]", "#alpha", "#eta"};
    TString branchNameData[2];
    TString branchNameNum[2];
    if (gasName=="P10") {
        branchNameData[0] = "tDrift";
        branchNameData[1] = "tGEM";
        branchNameNum[0] = "tDrift_Point";
        branchNameNum[1] = "tGEM_Point";
    }
    if (gasName=="CO2") {
        branchNameData[0] = "p50_r0_tDrift";
        branchNameData[1] = "p50_r0_tGEM";
        branchNameNum[0] = "p50_r0_tDrift_Point";
        branchNameNum[1] = "p50_r0_tGEM_Point";
    }

    for(int iType=0; iType<2; iType++)
    {
        /// naming
        int numPoints;
        double values[6][100];
        treeGas -> SetBranchAddress(branchNameNum[iType], &numPoints);
        treeGas -> SetBranchAddress(branchNameData[iType], &values);
        treeGas -> GetEntry(0);

        /// drawing
        auto nameCvs = Form("%s, %s",treeGas->GetName(),nameType[iType].Data());
        auto cvsAll = new TCanvas(nameCvs,treeGas->GetTitle(),2000,1000);
        cvsAll -> Divide(3,2);
        cout << nameCvs << " : " << numPoints << " points" << endl;

        for(int iProperty=0; iProperty<6; iProperty++)
        {
            auto graph = new TGraph();
            if (values[iProperty][0] < -100)
                continue;

            for(int iPoint=0; iPoint<numPoints; iPoint++)
            {
                auto value_y = values[iProperty][iPoint];
                auto value_efield = values[0][iPoint];

                /// ??
                if (value_y < 1.e-5 || values[iProperty][iPoint] > 1.e+7)
                    value_y = 0.;

                graph -> SetPoint(iPoint, value_efield, value_y);
            }

            /// drawing
            auto cvs = cvsAll -> cd(iProperty+1);
            cvs -> SetLeftMargin(0.12);
            graph -> SetTitle(Form("%s in %s;%s;%s", nameProperties[iProperty].Data(), nameType[iType].Data(), titleProperties[0].Data(), titleProperties[iProperty].Data()));
            graph -> SetMarkerStyle(20);
            graph -> Draw("apl");
            ///
        }
    }
}

void drawGas()
{
    auto file = new TFile("CO2BaseGasFiles.root", "read");

    TTree* tree1 = file -> Get<TTree>("P10");
    drawTree(tree1,"P10");

    TTree* tree2 = file -> Get<TTree>("CO2");
    drawTree(tree2,"CO2");
}
