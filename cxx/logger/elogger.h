#ifndef EJUNGWOOLOGGER_HH
#define EJUNGWOOLOGGER_HH

#include <iostream>
#include <fstream>
#include "TString.h"

#define e_logger(fileName) ejungwoo::ELogManager::RunLogger(fileName, false)
#define e_to_screen(val)   ejungwoo::ELogManager::SetLogToConsol(val)
#define e_to_file(val)     ejungwoo::ELogManager::SetLogToFile(val)

#define e_set_debug(val)   ejungwoo::ELogManager::SetPrintDebug(val)
#define e_set_cout(val)    ejungwoo::ELogManager::SetPrintCout(val)
#define e_set_info(val)    ejungwoo::ELogManager::SetPrintInfo(val)
#define e_set_warning(val) ejungwoo::ELogManager::SetPrintWarning(val)
#define e_set_error(val)   ejungwoo::ELogManager::SetPrintError(val)
#define e_set_list(val)    ejungwoo::ELogManager::SetPrintList(val)
#define e_set_test(val)    ejungwoo::ELogManager::SetPrintTest(val)

#define e_debug     ejungwoo::ELogger(__FILE__,__LINE__)
#define e_cout      ejungwoo::ELogger("","",0,1)
#define e_info      ejungwoo::ELogger("","",0,2)
#define e_warning   ejungwoo::ELogger("","",0,3)
#define e_error     ejungwoo::ELogger("","",0,4)
#define e_test      ejungwoo::ELogger("","",0,5)
#define e_list(i)   ejungwoo::ELogger("","",i,6)

namespace ejungwoo
{
    class ELogManager
    {
        private:
            static ELogManager *fLogManager;
            static TString fLogFileName;
            static std::ofstream fLogFile;
            static bool fLogToConsol;
            static bool fLogToFile;
            static bool fPrintDebug;
            static bool fPrintCout;
            static bool fPrintInfo;
            static bool fPrintWarning;
            static bool fPrintError;
            static bool fPrintList;
            static bool fPrintTest;
            static bool fPrintOutInnerParameter;
        public:
            ELogManager(TString fileName);
            static ELogManager* RunLogger(TString fileName="", bool forceNewLogger=false);
            static TString GetLogFileName();
            static std::ofstream& GetLogFile();
            static bool LogToConsol();
            static bool LogToFile();
            static void SetLogToConsol(bool val);
            static void SetLogToFile(bool val);
            static void SetPrintDebug(bool val);
            static void SetPrintCout(bool val);
            static void SetPrintInfo(bool val);
            static void SetPrintWarning(bool val);
            static void SetPrintError(bool val);
            static void SetPrintList(bool val);
            static void SetPrintTest(bool val);
            static bool PrintDebug();
            static bool PrintCout();
            static bool PrintInfo();
            static bool PrintWarning();
            static bool PrintError();
            static bool PrintList();
            static bool PrintTest();
            static void SetPrintOut(bool val); 
            static bool PrintOut();
    };

    class ELogger
    {
        public:
            ELogger(TString name, const std::string &title ,int rank, int option);
            ELogger(const std::string &title ,int line);
            template <class T> ELogger &operator<<(const T &v)
            {
                if (ELogManager::PrintOut())
                {
                    if (ELogManager::LogToConsol()) std::cout << v;
                    if (ELogManager::LogToFile()) ELogManager::GetLogFile() << v;
                }
                return *this;
            }
            ELogger &operator<<(std::ostream&(*f)(std::ostream&))
            {
                if (ELogManager::PrintOut())
                {
                    if (ELogManager::LogToConsol()) std::cout << *f;
                    if (ELogManager::LogToFile()) ELogManager::GetLogFile() << *f;
                }
                return *this;
            }
    };

    ELogManager* ELogManager::fLogManager = nullptr;
    TString ELogManager::fLogFileName = "";
    std::ofstream ELogManager::fLogFile;
    bool ELogManager::fLogToConsol = true;
    bool ELogManager::fLogToFile = false;

    ELogManager::ELogManager(TString fileName)
    {
        fLogManager = this;
        if (fileName.IsNull())
            fileName = "auto_created_logger.log";
        fLogToFile = true;
        ELogManager::fLogFileName = fileName;
        fLogFile.open(fileName);
        std::cout << "Log file is set: " << fileName << std::endl;
    }

    ELogManager* ELogManager::RunLogger(TString fileName, bool forceNewLogger)
    {
        if (fLogManager != nullptr) {
            std::cout << "Logger is already running :" << ELogManager::fLogFileName << std::endl;
            if (forceNewLogger) {
                std::cout << "forceNewLogger flag is set. Creating new logger " << fileName << std::endl;
                return new ELogManager(fileName);
            }
            return fLogManager;
        }
        return new ELogManager(fileName);
    }

    TString ELogManager::GetLogFileName()    { return fLogFileName; }
    std::ofstream& ELogManager::GetLogFile() { return fLogFile; }
    bool ELogManager::LogToConsol()  { return fLogToConsol; }
    bool ELogManager::LogToFile()    { return fLogToFile; }
    void ELogManager::SetLogToConsol (bool val) { fLogToConsol = val; }
    void ELogManager::SetLogToFile   (bool val) { fLogToFile = val; }
    bool ELogManager::fPrintDebug    = true;
    bool ELogManager::fPrintCout     = true;
    bool ELogManager::fPrintInfo     = true;
    bool ELogManager::fPrintWarning  = true;
    bool ELogManager::fPrintError    = true;
    bool ELogManager::fPrintList     = true;
    bool ELogManager::fPrintTest     = true;
    bool ELogManager::fPrintOutInnerParameter = true;
    void ELogManager::SetPrintDebug  (bool val) { fPrintDebug = val; }
    void ELogManager::SetPrintCout   (bool val) { fPrintCout = val; }
    void ELogManager::SetPrintInfo   (bool val) { fPrintInfo = val; }
    void ELogManager::SetPrintWarning(bool val) { fPrintWarning = val; }
    void ELogManager::SetPrintError  (bool val) { fPrintError = val; }
    void ELogManager::SetPrintList   (bool val) { fPrintList = val; }
    void ELogManager::SetPrintTest   (bool val) { fPrintTest = val; }
    bool ELogManager::PrintDebug()   { return fPrintDebug; }
    bool ELogManager::PrintCout()    { return fPrintCout; }
    bool ELogManager::PrintInfo()    { return fPrintInfo; }
    bool ELogManager::PrintWarning() { return fPrintWarning; }
    bool ELogManager::PrintError()   { return fPrintError; }
    bool ELogManager::PrintList()    { return fPrintList; }
    bool ELogManager::PrintTest()    { return fPrintTest; }
    bool ELogManager::PrintOut()     { return fPrintOutInnerParameter; }
    void ELogManager::SetPrintOut(bool val) { fPrintOutInnerParameter = val; } 

    ELogger::ELogger(TString name, const std::string &title ,int rank, int option)
    {
        if (option == 0)
            return;
        TString header;
        if (!name.IsNull()) {
            for (auto i=0; i<rank; ++i)
                header = header + "  ";
            header = header + Form("[%s::%s] ", name.Data(), title.c_str());
        }
        switch (option)
        {
            case 1:  (ELogManager::PrintCout())   ? ELogManager::SetPrintOut(true) : ELogManager::SetPrintOut(false); break;
            case 2:  (ELogManager::PrintInfo())   ? ELogManager::SetPrintOut(true) : ELogManager::SetPrintOut(false); break;
            case 3:  (ELogManager::PrintWarning())? ELogManager::SetPrintOut(true) : ELogManager::SetPrintOut(false); break;
            case 4:  (ELogManager::PrintError())  ? ELogManager::SetPrintOut(true) : ELogManager::SetPrintOut(false); break;
            case 5:  (ELogManager::PrintTest())   ? ELogManager::SetPrintOut(true) : ELogManager::SetPrintOut(false); break;
            case 6:  (ELogManager::PrintList())   ? ELogManager::SetPrintOut(true) : ELogManager::SetPrintOut(false); break;
            default: ;
        }
        if (ELogManager::LogToConsol())
        {
            switch (option)
            {
                case 1:  if (ELogManager::PrintOut()) std::cout << header; break;
                case 2:  if (ELogManager::PrintOut()) std::cout << header << "\033[0;32m" << "info> "   << "\033[0m"; break;
                case 3:  if (ELogManager::PrintOut()) std::cout << header << "\033[0;33m" << "warning> "<< "\033[0m"; break;
                case 4:  if (ELogManager::PrintOut()) std::cout << header << "\033[0;31m" << "error> "  << "\033[0m"; break;
                case 5:  if (ELogManager::PrintOut()) std::cout << header << "\033[0;36m" << "test> "   << "\033[0m"; break;
                case 6:  if (ELogManager::PrintOut()) std::cout << header << "\033[0;34m" << std::right << std::setw(3) << rank << ". " << "\033[0m"; break;
                default: ;
            }
        }
        if (ELogManager::LogToFile())
        {
            switch (option)
            {
                case 1:  if (ELogManager::PrintOut()) ELogManager::GetLogFile() << header; break;
                case 2:  if (ELogManager::PrintOut()) ELogManager::GetLogFile() << header << "info> "; break;
                case 3:  if (ELogManager::PrintOut()) ELogManager::GetLogFile() << header << "warning> "; break;
                case 4:  if (ELogManager::PrintOut()) ELogManager::GetLogFile() << header << "error> "; break;
                case 5:  if (ELogManager::PrintOut()) ELogManager::GetLogFile() << header << "test> "; break;
                case 6:  if (ELogManager::PrintOut()) ELogManager::GetLogFile() << header << std::right << std::setw(3) << rank << " "; break;
                default: ;
            }
        }
    }

    ELogger::ELogger(const std::string &title ,int line)
    {
        (ELogManager::PrintDebug()) ? ELogManager::SetPrintOut(true) : ELogManager::SetPrintOut(false);

        if (ELogManager::PrintOut())
        {
            if (ELogManager::LogToConsol())
                std::cout<<"+\033[0;36m"<<Form("%d ",line)<<"\033[0m "<<Form("%s \033[0;36m#\033[0m ", title.c_str());
            if (ELogManager::LogToFile())
                ELogManager::GetLogFile()<<"+"<<Form("%d ",line)<<" "<<Form("%s # ", title.c_str());
        }
    }
};

#endif
