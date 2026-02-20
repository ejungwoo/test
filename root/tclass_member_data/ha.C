TObjArray* collect_dm(TClass *givenClass, TObjArray *dmArray=nullptr, int depth=0);

void check_data()
{
    auto file = new TFile("data_reco/stark_0199.channel.root");
    auto tree = (TTree*) file -> Get("event");
    TClonesArray *array = nullptr;
    tree -> SetBranchAddress("SiChannel",&array);

    TClass *myClass = TClass::GetClass("LKSiChannel");
    //TClass *myClass = TClass::GetClass("LKMCTagged");
    //TClass *myClass = TClass::GetClass("LKRun");
    auto dmArray = collect_dm(myClass);
    TDataMember *dm;
    Longptr_t retVal = 0;

    std::vector<int      > listInt     ;
    std::vector<UInt_t   > listUInt    ;
    std::vector<Short_t  > listShort   ;
    std::vector<UShort_t > listUShort  ;
    std::vector<Long64_t > listLong64  ;
    std::vector<ULong64_t> listULong64 ;
    std::vector<bool     > listBool    ;
    std::vector<float    > listFloat   ;
    std::vector<double   > listDouble  ;
    std::vector<TVector3 > listTVector3;

    auto numDM = dmArray -> GetEntries();
    for (auto iDM=0; iDM<numDM; ++iDM)
    {
        dm = (TDataMember*) dmArray -> At(iDM);
        TString data_name = dm -> GetName();
        TString data_type = dm -> GetFullTypeName();
        //TString data_type2 = dm -> GetTrueTypeName();
        TString data_clss = dm -> GetClass() -> GetName();
        //cout << data_type << " " << data_type2 << endl;
        //cout << data_type << " " << data_name << " (" << data_clss << ")" << endl;
        if (data_clss=="TObject" || data_type=="atomic_TClass_ptr" || data_type.EndsWith("*"))
            dmArray -> Remove(dm);
    }
    dmArray -> Compress();
    //numDM = dmArray -> GetEntries();
    //for (auto iDM=0; iDM<numDM; ++iDM)
    //{
    //    dm = (TDataMember*) dmArray -> At(iDM);
    //    TString data_type = dm -> GetFullTypeName();
    //}
    TIter next_dm(dmArray);

    auto numEvents = tree -> GetEntries();
    for (auto iEvent=0; iEvent<numEvents; ++iEvent)
    {
        tree -> GetEntry(iEvent);
        auto numChannels = array -> GetEntries();
        for (auto iChannel=0; iChannel<numChannels; ++iChannel)
        {
            auto channel = (LKSiChannel*) array -> At(iChannel);
            //auto channel = array -> At(iChannel);

            channel -> Print();

            //next_data.Reset();
            //while ((dm = (TDataMember*)next_data()))
            next_dm.Reset();
            while ((dm = (TDataMember*)next_dm()))
            {
                TString data_name = dm -> GetName();
                //TString data_name = dm -> GetTitle();
                TString data_type = dm -> GetFullTypeName();
                //TString data_type = dm -> GetTrueTypeName();
                TString data_clss = dm -> GetClass() -> GetName();
                TMethodCall* call = dm -> GetterMethod();
                if (call!=nullptr)
                {
                    TString data_gett = call -> GetMethodName();
                    cout << channel -> IsA() -> GetClassMethod(data_gett) << endl;
                    //Longptr_t retVal;
                    Double_t retVal;
                    call->Execute(channel, retVal);
                    Double_t retDouble;
                    call->Execute(channel, retDouble);
                    //call->Execute(retDouble);
                    std::cout
                        << setw(22) << data_clss
                        << setw(22) << data_type
                        << setw(22) << data_name
                        << setw(22) << data_gett << " ";

                    //if (data_type == "Int_t" || data_type == "int") {
                    //    //int val = *(int*)voidp;//static_cast<int>(retVal);
                    //    //int* val = reinterpret_cast<int*>(&retVal);
                    //    //long* ptr_long = &retVal;/* ... initialize with address of an int ... */;
                    //    //int val = (int)*ptr_long;
                    //    int val = static_cast<int>(retVal);
                    //    std::cout << " (int) " << val << std::endl;
                    //}
                    if (data_type == "Double_t" || data_type == "double") {
                        //double val = static_cast<double>(retVal);
                        //double val = static_cast<double>(retDouble);
                        double val = retDouble;
                        std::cout << " " << val << std::endl;
                    }
                    //else if (data_type == "UInt_t" || data_type == "unsigned int") {
                    //    unsigned int val = static_cast<unsigned int>(retVal);
                    //    std::cout << " " << val << std::endl;
                    //}
                    //else if (data_type == "Short_t" || data_type == "short") {
                    //    short val = static_cast<short>(retVal);
                    //    std::cout << " " << val << std::endl;
                    //}
                    //else if (data_type == "UShort_t" || data_type == "unsigned short") {
                    //    unsigned short val = static_cast<unsigned short>(retVal);
                    //    std::cout << " " << val << std::endl;
                    //}
                    //else if (data_type == "Long64_t" || data_type == "long long") {
                    //    long long val = static_cast<long long>(retVal);
                    //    std::cout << " " << val << std::endl;
                    //}
                    //else if (data_type == "ULong64_t" || data_type == "unsigned long long") {
                    //    unsigned long long val = static_cast<unsigned long long>(retVal);
                    //    std::cout << " " << val << std::endl;
                    //}
                    //else if (data_type == "Bool_t" || data_type == "bool") {
                    //    bool val = static_cast<bool>(retVal);
                    //    std::cout << " " << val << std::endl;
                    //}
                    //else if (data_type == "Float_t" || data_type == "float") {
                    //    float val = static_cast<float>(retVal);
                    //    std::cout << " " << val << std::endl;
                    //}
                    //else if (data_type == "TVector3") {
                    //    const TVector3* v = static_cast<const TVector3*>(retVal);
                    //    std::cout << " " << v->X() << ", " << v->Y() << ", " << v->Z() << std::endl;
                    //}
                    else {
                        std::cout << std::endl;
                    }

                }
                else {
                    std::cout
                        << setw(22) << data_clss
                        << setw(22) << data_type
                        << setw(22) << data_name << endl;
                }
            }

            return;
        }
    }

}

TObjArray* collect_dm(TClass *givenClass, TObjArray *dmArray, int depth)
{
    {
        for (auto i=0; i<depth; ++i) std::cout << "  ";
        std::cout << givenClass->GetName() << endl;
    }

    if (dmArray==nullptr)
        dmArray = new TObjArray();

    TDataMember *dm;
    TIter next_data(givenClass->GetListOfDataMembers());
    while ((dm = (TDataMember*)next_data()))
        dmArray -> Add(dm);

    /////////////////////////////////////////////////////////////////////

    TBaseClass *base;
    auto listBases = givenClass -> GetListOfBases();
    if (listBases->GetEntries()==0)
        return (TObjArray*) nullptr;

    TIter next_base(listBases);
    while ((base = (TBaseClass*)next_base())) {
        TClass *baseClass = base->GetClassPointer();
        if (!baseClass) continue;
        collect_dm(baseClass, dmArray, depth+1);
    }
    return dmArray;
}
