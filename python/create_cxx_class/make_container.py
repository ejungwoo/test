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
+bname  rawData

-private    Int_t   mmMul;
-private    Float_t mmEnergy[1030];   ///[mmMul]
-private    Int_t   mmWaveformY[1030][512];   ///[mmMul][time]
-private    int kLeftStrip   = 0;
-private    Int_t type[3][4][4][68];
-private    Int_t DetLoc[3][4][4][68];
-private    const Int_t mmnum = 1024; /// # of all channels
-private    int dummy;
-par
"""
).print_task(to_screen=to_screen,to_file=to_file)
