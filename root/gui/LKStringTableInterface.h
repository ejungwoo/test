#ifndef LILAKSTRINGTABLEINTERFACE_HH
#define LILAKSTRINGTABLEINTERFACE_HH

#include <vector>
#include "TString.h"
#include "TVirtualTableInterface.h"
#include "LKParameterContainer.h"

class LKStringTableInterface : public TVirtualTableInterface
{
    private:
        std::vector<std::vector<TString>> fData;
        std::vector<TString> fColumnTitles;
        UInt_t fNumColumns = 0;
        UInt_t fNumRows = 0;

    public:
        LKStringTableInterface(UInt_t nr, UInt_t nc);
        LKStringTableInterface(UInt_t nr, UInt_t nc, TString ctitles);

        void SetTableSize(UInt_t nr, UInt_t nc);
        void SetRowSize(UInt_t nr) { SetTableSize(nr, fNumColumns); }
        void SetColumnSize(UInt_t nc) { SetTableSize(fNumRows, nc); }
        void SetColumnTitles(TString titles);

        UInt_t GetNRows() override { return fData.size(); }
        UInt_t GetNColumns() override { return fData.empty() ? 0 : fData[0].size(); }
        Double_t GetValue(UInt_t, UInt_t) override { return 0.0; }
        const char *GetValueAsString(UInt_t row, UInt_t col) override;
        const char *GetRowHeader(UInt_t row) override;
        const char *GetColumnHeader(UInt_t col) override;

        void SetText(UInt_t row, UInt_t col, const TString &val);
        bool ReadParameterContainer(LKParameterContainer *par);
};

#endif
