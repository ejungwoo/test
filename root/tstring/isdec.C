bool CheckFloat(TString formula);
bool CheckInteger(TString formula);

void isdec()
{
    TString examples[] = {
        "0",
        "10",
        "-99",
        "-22",
        "0.1",
        "-0.1"
        "5+4",
        "2 3",
        "+5 4",
    };

    for (auto value : examples)
    {
        bool i1 = value.IsAlnum();
        bool i2 = value.IsBin();
        bool i3 = value.IsDec();
        bool i4 = value.IsDigit();
        bool i5 = value.IsHex();
        bool i6 = value.IsOct();
        bool i7 = CheckFloat(value);
        bool i8 = CheckInteger(value);
        cout << value << endl;
        cout << "- IsAlnum= " << i1 << endl;
        cout << "- IsBin  = " << i2 << endl;
        cout << "- IsDec  = " << i3 << endl;
        cout << "- IsDigit= " << i4 << endl;
        cout << "- IsHex  = " << i5 << endl;
        cout << "- IsOct  = " << i6 << endl;
        cout << "- Float  = " << i7 << endl;
        cout << "- Integer= " << i8 << endl;
        cout << endl;
    }
}

bool CheckFloat  (TString formula) { return std::regex_match(formula.Data(), std::regex("^[0-9\\(\\)\\+\\-\\*/Ee\\.]+$")); }
bool CheckInteger(TString formula) { return std::regex_match(formula.Data(), std::regex("^[\\+\\-]?[0-9]+$")); }
