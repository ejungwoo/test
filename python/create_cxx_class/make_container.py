from lilakcc import lilakcc

to_screen=False
to_file=True

################################################################################################### 
cc = lilakcc()

cc.add("""
+class GETChannel : public LKContainer
+public     Int_t   fMult = -1;
+public     Int_t   fEventIdx = -1;
+public     Int_t   fFrameNo = -1;
+public     Int_t   fDecayNo = -1;
+public     Int_t   fCobo = -1;
+public     Int_t   fAsad = -1;
+public     Int_t   fAget = -1;
+public     Int_t   fChan = -1;
+public     Float_t fTime = -1;
+public     Float_t fEnergy = -1;
+public     Int_t   fWaveformX[512];
+init       for (auto i=0; i<512; ++i) fWaveformX[i] = -1;
+public     Int_t   fWaveformY[512];
+init       for (auto i=0; i<512; ++i) fWaveformY[i] = -1;
""")

cc.print_container(to_screen=to_screen,to_file=to_file)
#+gname  -- set global parameter name
#+lname  -- set local  parameter name
#+pname  -- set parameter name to be used in the parameter container
#+persis -- set persistency of parameter (True or False). Default is True
#+setter -- set setter
#+getter -- set getter
#+source -- set content to be included in the Constructor of LKTask
#+init   -- set content to be included in the Init() method of LKTask
#+clear  -- set content to be included in the Clear() method of LKTask
#+print  -- set content to be included in the Print() method of LKTask
#+copy   -- set content to be included in the Copy() method of LKTask
