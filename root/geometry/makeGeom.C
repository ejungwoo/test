void makeGeom()
{
  //--- Definition of a simple geometry
  //   gSystem->Load("libGeom");
   new TGeoManager("genfitGeom", "GENFIT geometry");


   unsigned int medInd(0);
   Double_t mPar[10];
   //TAG sollte wieder 0 werden sens flag
   mPar[0]=0.;//sensitive volume flag
   mPar[1]=1.;//magnetic field flag
   mPar[2]=30.;//max fiel in kGauss
   mPar[3]=0.1;//maximal angular dev. due to field
   mPar[4]=0.01;//max step allowed (in cm)
   mPar[5]=1.e-5;//max fractional energy loss
   mPar[6]=1.e-3;//boundary crossing accuracy
   mPar[7]=1.e-5;//minimum step
   mPar[8]=0.;//not defined
   mPar[9]=0.;//not defined

   TGeoMaterial *siliconMat = new TGeoMaterial("siliconMat",28.0855,14.,2.329);
   siliconMat->SetRadLen(1.);//calc automatically, need this for elemental mats.
   // cppcheck-suppress unreadVariable
   TGeoMedium *silicon = new TGeoMedium("silicon",medInd++,siliconMat,mPar);

   TGeoMixture *vacuumMat = new TGeoMixture("vacuumMat",3);
   vacuumMat->AddElement(14.01,7.,.78);
   vacuumMat->AddElement(16.00,8.,.21);
   vacuumMat->AddElement(39.95,18.,.01);
   vacuumMat->SetDensity(1.2e-15);
   // cppcheck-suppress unreadVariable
   TGeoMedium *vacuum = new TGeoMedium("vacuum",medInd++,vacuumMat,mPar);

   TGeoVolume *top = gGeoManager->MakeBox("TOPPER", vacuum, 1000., 1000., 1000.);
   gGeoManager->SetTopVolume(top); // mandatory !

   double thickness = 0.05;
   double distance = 1;

   // Detector dimensions (cm)
   double dx = 5.0;   // 100 mm
   double dy = 5.0;   // 100 mm
   double dz = 0.05;  // 1 mm
   double zSpacing = 1.0; // space between layers (cm)
   int nLayers = 10;

   for (int i = 0; i < nLayers; ++i)
   {
       TString volName = Form("siliconLayer_%d", i);
       TGeoVolume* siliconLayer = gGeoManager->MakeBox(volName, silicon, dx, dy, dz);
       siliconLayer->SetLineColor(kGreen + 2);

       double zPos = -((nLayers - 1) * zSpacing) / 2. + i * zSpacing;
       top->AddNode(siliconLayer, i, new TGeoTranslation(0, 0, zPos));
   }

   //--- close the geometry
   gGeoManager->CloseGeometry();

   //--- draw the ROOT box
   gGeoManager->SetVisLevel(10);
   //top->Draw("ogl");
   //TFile *outfile = TFile::Open("genfitGeom.root","RECREATE");
   //gGeoManager->Write();
   //outfile->Close();
   top -> Draw("ogl");
}
