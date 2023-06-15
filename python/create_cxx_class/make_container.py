from lilakcc import lilakcc

################################################################################################### 
lilakcc(
"""
/// TexAT
+class TexAT2
"""
).print_detector()

################################################################################################### 
lilakcc(
"""
/// Raw event data from GET
+class MMChannel
+public     Int_t   fFrameNo = -1;
+public     Int_t   fDecayNo = -1;
+public     Int_t   fCobo = -1;
+public     Int_t   fAsad = -1;
+public     Int_t   fAget = -1;
+public     Int_t   fChan = -1;
+public     Float_t fTime = -1;
+public     Float_t fEnergy = -1;
+public     Int_t   fWaveformX[512];
+clear      for (auto i=0; i<512; ++i) fWaveformX[i] = -1;
+getter     Int_t *GetWaveformX() { return fWaveformX; }
+setter     void SetWaveformX(Int_t *waveform) { memcpy(fWaveformX, waveform, sizeof(Int_t)*512); }
+public     Int_t   fWaveformY[512];
+clear      for (auto i=0; i<512; ++i) fWaveformY[i] = -1;
+getter     Int_t *GetWaveformY() { return fWaveformY; }
+setter     void SetWaveformY(Int_t *waveform) { memcpy(fWaveformY, waveform, sizeof(Int_t)*512); }
"""
).print_container()

################################################################################################### 
lilakcc(
"""
-class TTRootConversionTask
/// Simple conversion from pre-converted root file
-odata  auto fChannelArray = new TClonesArray("GETChannel",200)
-bname  RawData
-private TFile* fInputFile;
-private TTree* fInputTree;
-enum eType
    kLeftStrip   // 0
    kRightStrip  // 1
    kLeftChain   // 2
    kRightChain  // 3
    kLowCenter   // 4
    kHighCenter  // 5
    kForwardSi   // 6
    kForwardCsI  // 7
    kMMJr        // 8
    kCENSX6      // 10
    kCENSCsI     // 11
    kExternal    // 100
-enum eDetLoc
    kLeft          // 0
    kRight         // 1
    kCenterFront   // 2
    kBottomLeftX6  // 10
    kBottomRightX6 // 11
    kCsI           // -1
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
-private Int_t Type[3][4][4][68];
-private Int_t DetLoc[3][4][4][68];
-private const Int_t mmnum = 1024; // # of all channels
-private const Int_t sinum = 45; // quadrant*9
-private const Int_t X6num = 600; // 20chan*30det
-private const Int_t CsInum = 64; // 1chan*64det
+private TString fInputFileName = /home/ejungwoo/data/texat/run_0824.dat.19-03-23_23h42m36s.38.root 
+private TString fmapmmFileName = /home/ejungwoo/data/txtfiles/mapchantomm.txt
+private TString fmapsiFileName = /home/ejungwoo/data/txtfiles/mapchantosi_CRIB.txt
+private TString fmapX6FileName = /home/ejungwoo/data/txtfiles/mapchantoX6_CRIB.txt
+private TString fmapCsIFileName = /home/ejungwoo/data/txtfiles/mapchantoCsI_CRIB.txt 
"""
).print_task()

