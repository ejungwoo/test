void test()
{
    const char *selection = "EventHeader[0].fIsGoodEvent";
    //const char *selection = "1";

    auto file = new TFile("~/data/texat/reco/texat_0801.all.root");
    auto tree = (TTree*) file -> Get("event");

    tree -> Draw(">>ha",selection,"entrylist");
    TEventList *elist = (TEventList*)gDirectory->Get("ha");
    elist -> ls();
    return;

    auto fSelect = new TTreeFormula("LKTTreeSelection",selection,tree);

    Int_t tnumber = -1;
    auto numEntries = tree -> GetEntries();
    //for (auto entry=0; entry<numEntries; ++entry)
    //for (auto entry=0; entry<10; ++entry)
    for (auto entry=0; entry<10; ++entry)
    {
        auto entryNumber = tree->GetEntryNumber(entry);
        //lk_debug << entry << " " << entryNumber << endl;
        if (entryNumber < 0) break;
        Long64_t localEntry = tree -> LoadTree(entryNumber);

        if (localEntry < 0) break;
        if (tnumber != tree->GetTreeNumber()) {
            tnumber = tree->GetTreeNumber();
            if (fSelect) fSelect->UpdateFormulaLeaves();
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


    //cout << ndata << endl;
}
