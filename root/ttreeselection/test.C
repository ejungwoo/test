void test()
{
    const char *selection = "EventHeader[0].fIsGoodEvent";
    //const char *selection = "Entry$==2";
    //const char *selection = "1";

    auto file = new TFile("~/data/texat/reco/texat_0801.all.root");
    auto fInputTree = (TTree*) file -> Get("event");
    TClonesArray* fEventHeaderHolder = nullptr;
    fInputTree -> SetBranchAddress("EventHeader",&fEventHeaderHolder);

    fInputTree -> Draw(">>lkentrylist",selection,"entrylist");
    TEntryList *entryList = (TEntryList*) gDirectory -> Get("lkentrylist");
    Long64_t numSelEntries = entryList -> GetN();
    Long64_t chainEntries = fInputTree -> GetEntries();
    Int_t fTreeNumber = -1;
    fInputTree -> SetEntryList(entryList);

    //for (auto iSelEntry=0; iSelEntry<numSelEntries; ++iSelEntry)
    for (auto iSelEntry=0; iSelEntry<100; ++iSelEntry)
    {
        auto entryNumber = fInputTree -> GetEntryNumber(iSelEntry);
        if (entryNumber<0) {
            cout << "entryNumber<0" << endl;
            break;
        }
        auto localEntry = fInputTree -> LoadTree(entryNumber);
        if (localEntry<0) {
            cout << "localEntry<0" << endl;
            break;
        }
        fInputTree -> GetEntry(entryNumber);
        cout << iSelEntry << " " << entryNumber << " " << localEntry << endl;
        auto eventHeader = (TTEventHeader*) fEventHeaderHolder -> At(0);
        cout << eventHeader << endl;
        eventHeader -> Print();
    }

    /*
    auto fSelect = new TTreeFormula("LKTTreeSelection",selection,fInputTree);

    Int_t fTreeNumber = -1;
    auto numEntries = fInputTree -> GetEntries();
    //for (auto entry=0; entry<numEntries; ++entry)
    //for (auto entry=0; entry<10; ++entry)
    for (auto entry=0; entry<10; ++entry)
    {
        auto entryNumber = fInputTree > GetEntryNumber(entry);
        //lk_debug << entry << " " << entryNumber << endl;
        if (entryNumber < 0) break;
        Long64_t localEntry = fInputTree -> LoadTree(entryNumber);

        if (localEntry < 0) break;
        if (fTreeNumber != fInputTree->GetTreeNumber()) {
            fTreeNumber = fInputTree -> GetTreeNumber();
            if (fSelect) fSelect -> UpdateFormulaLeaves();
        }

        if (fSelect){
            Int_t ndata = fSelect -> GetNdata();
            Bool_t keep = kFALSE;
            for(Int_t current = 0; current<ndata && !keep; current++) {
                //lk_debug << (fSelect -> EvalInstance(current) != 0) << endl;
                keep |= (fSelect -> EvalInstance(current) != 0);
            }
            //if (!keep) continue;
            //lk_debug << ">> " << entry << " " << keep << endl;
        }
    }
    */
}
