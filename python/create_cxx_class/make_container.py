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
"""
).print_task(to_screen=to_screen,to_file=to_file)
