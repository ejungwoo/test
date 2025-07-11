#include "LKStringTableInterface.h"

LKStringTableInterface::LKStringTableInterface(UInt_t nr, UInt_t nc)
{
    SetTableSize(nr,nc);
}

LKStringTableInterface::LKStringTableInterface(UInt_t nr, UInt_t nc, TString ctitles)
{ SetTableSize(nr,nc);
    SetColumnTitles(ctitles);
}

void LKStringTableInterface::SetTableSize(UInt_t nr, UInt_t nc)
{
    if (fNumRows==nr&&fNumColumns==nc)
        return;
    fNumRows = nr;
    fNumColumns = nc;
    //fData.resize(fNumRows, std::vector<TString>(fNumColumns));
    fData.resize(fNumRows);
    for (auto &row : fData)
        row.resize(fNumColumns);
    fColumnTitles.resize(fNumRows);
    for (UInt_t r=0; r<nr; ++r) {
        for (UInt_t c=0; c<nc; ++c) {
            fData[r][c] = "";
        }
    }
    for (UInt_t c=0; c<nc; ++c) {
        fColumnTitles[c].Form("%d",c);
    }
}

void LKStringTableInterface::SetColumnTitles(TString titles)
{
    auto array = titles.Tokenize(":");
    for (UInt_t c=0; c<fNumColumns; ++c)
    {
        auto block = (TObjString*) array -> At(c);
        if (block!=nullptr) {
            TString title = block -> GetString();
            fColumnTitles[c] = title;
            lk_debug << title << endl;
        }
    }
}

const char *LKStringTableInterface::GetValueAsString(UInt_t row, UInt_t col)
{
    if (row >= fData.size() || col >= fData[row].size())
        return "";
    return fData[row][col];
}

const char *LKStringTableInterface::GetRowHeader(UInt_t row)
{
    return Form("%d",row);
}

const char *LKStringTableInterface::GetColumnHeader(UInt_t col)
{
    if (col >= fColumnTitles.size())
        return "";
    return fColumnTitles[col];
}

void LKStringTableInterface::SetText(UInt_t row, UInt_t col, const TString &val)
{
    if (row >= fData.size() || col >= fData[row].size())
        return;
    fData[row][col] = val;
}

bool LKStringTableInterface::ReadParameterContainer(LKParameterContainer *par)
{
    SetColumnTitles("type:group:name:raw:value:comment");
    TIter iterator(par);
    LKParameter *parameter;
    int numPar = par -> GetEntries();;
    SetTableSize(numPar,6);
    int count = 0;
    while ((parameter = dynamic_cast<LKParameter*>(iterator())))
    {
        TString type = "?";
        TString group = parameter -> GetGroup();
        TString name = parameter -> GetMainName();
        TString raw = parameter -> GetRaw();
        TString value = parameter -> GetValue();
        TString comment = parameter -> GetComment();
        if      (parameter->IsStandard()   ) type = "Standard";   //"Standard";
        else if (parameter->IsLegacy()     ) type = "Legacy";     //"Legacy";
        else if (parameter->IsRewrite()    ) type = "Rewrite";    //"Rewrite";
        else if (parameter->IsMultiple()   ) type = "Multiple";   //"Multiple";
        else if (parameter->IsTemporary()  ) type = "Temporary";  //"Temporary";
        else if (parameter->IsInputFile()  ) type = "InputFile";  //"InputFile";
        else if (parameter->IsConditional()) type = "Conditional";//"Conditional";
        else if (parameter->IsLineComment()) type = "LineComment";//"LineComment";
        else if (parameter->IsCommentOut() ) type = "CommentOut"; //"CommentOut";
        fData[count][0] = type;
        fData[count][1] = group;
        fData[count][2] = name;
        fData[count][3] = raw;
        fData[count][4] = value;
        fData[count][5] = comment;
        //lk_debug << type << " " << group << " " << name << "  "<< raw << " " << value << " " << comment << endl;
        count++;
    }

    return true;
}
