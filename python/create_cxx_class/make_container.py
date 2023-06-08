from lilakcc import lilakcc

to_screen=False
to_file=True

################################################################################################### 
#lilakcc(
#"""
#/// Raw event data from GET
#+class GETChannel
#
#+public     Int_t   fMult = -1;
#+public     Int_t   fEventIdx = -1;
#+public     Int_t   fFrameNo = -1;
#+public     Int_t   fDecayNo = -1;
#+public     Int_t   fCobo = -1;
#+public     Int_t   fAsad = -1;
#+public     Int_t   fAget = -1;
#+public     Int_t   fChan = -1;
#+public     Float_t fTime = -1;
#+public     Float_t fEnergy = -1;
#
#+public     Int_t   fWaveformX[512];
#+clear      for (auto i=0; i<512; ++i) fWaveformX[i] = -1;
#+getter     Double_t *GetWaveformX() { return fWaveformX; }
#+setter     void SetBufferIn(Double_t *waveform) { memcpy(fWaveformX, waveform, sizeof(Double_t)*512); }
#
#+public     Int_t   fWaveformY[512];
#+clear      for (auto i=0; i<512; ++i) fWaveformY[i] = -1;
#+getter     Double_t *GetWaveformY() { return fWaveformY; }
#+setter     void SetBufferIn(Double_t *waveform) { memcpy(fWaveformY, waveform, sizeof(Double_t)*512); }
#"""
#).print_container(to_screen=to_screen,to_file=to_file)


################################################################################################### 
lilakcc(
"""
+class ATConversionTask
/// Simple conversion from pre-converted root file

+odata  auto fChannelArray = new TClonesArray("GETChannel",200)
+bname  RawData

+private TString fInputFileName = "~/data/texat/run_0824.dat.19-03-23_23h42m36s.38.root";
-private TFile* fInputFile;
-private TTree* fInputTree;

-private Int_t   mmMul;
-private Int_t   mmHit;
-private Int_t   mmEventIdx;
-private Int_t   mmFrameNo[1030];   //[mmMul]
-private Int_t   mmDecayNo[1030];   //[mmMul]
-private Int_t   mmCobo[1030];   //[mmMul]
-private Int_t   mmAsad[1030];   //[mmMul]
-private Int_t   mmAget[1030];   //[mmMul]
-private Int_t   mmChan[1030];   //[mmMul]
-private Float_t mmTime[1030];   //[mmMul]
-private Float_t mmEnergy[1030];   //[mmMul]
-private Int_t   mmWaveformX[1030][512];   //[mmMul][time]
-private Int_t   mmWaveformY[1030][512];   //[mmMul][time]
"""
).print_task(to_screen=to_screen,to_file=to_file)
