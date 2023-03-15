#ifndef LKLOGGER_HH
#define LKLOGGER_HH

#include <iostream>
#include <fstream>
#include "TString.h"
#include "LKCompiled.h"
#include "LKLogger.hh"

/// lilak logger shortcut macros
#define lk_logger(logFileName) LKLogManager::RunLogger(logFileName)
#define lk_logger_name() LKLogManager::GetLogFileName()

/**
 * You may remove this comment block after reading it through
 *
 * Example LILAK container class
 *
 * Essential: 
 *  - inherit LKContainer as public.
 *  - Write constructor containing Clear() method.
 *  - Write Clear() method.
 *
 * More about Clear() method:
 * It is recommended that LKTasks create data container array using TClonesArray class.
 * For the detail of TClonesArray, see https://root.cern/doc/master/classTClonesArray.html
 * or https://opentutorials.org/module/2860/19477 (for the simple version in Korean)
 * In LKTask, Clear("C") is called to TClonesArray at the start of the Exec() of LKTask classes.
 * This means that all containers 
 *
 * Version number (2nd par. in ClassDef of source file) should be updated if the class has been modified.
 * This notifiy users that the container has been update in the new LILAK (or side project version).
 *
 * Recommended:
 *  - Print() to see what is inside the container;
 *  - Doxygen style documentaion.
 *    You may use "///<" after the member parameter or function definition.
 *    For multi-line comments, use two stars "**" at the start of the comment instead of one star "*".
 */
class LKLogManager
{
  private:
    static LKLogManager *fLogManager;
    static TString fLogFileName;
    static std::ofstream fLogFile;
    static bool fLogToConsol;
    static bool fLogToFile;

  public:
    LKLogManager(TString fileName);
    static LKLogManager* RunLogger(TString fileName="");
    static TString GetLogFileName();
    static std::ofstream& GetLogFile();
    static bool LogToConsol();
    static bool LogToFile();
};

/// lilak debug logger
#define lk_debug   LKLogger(__FILE__,__LINE__)

/// lilak logger
#define lk_cout    LKLogger(fName,__FUNCTION__,fRank,1)
#define lk_info    LKLogger(fName,__FUNCTION__,fRank,2)
#define lk_warning LKLogger(fName,__FUNCTION__,fRank,3)
#define lk_error   LKLogger(fName,__FUNCTION__,fRank,4)

/// lilak logger for non-LKGear classes and macros. These will not create line-header
#define lx_cout     LKLogger("","",0,1)
#define lx_info     LKLogger("","",0,2)
#define lx_warning  LKLogger("","",0,3)
#define lx_error    LKLogger("","",0,4)

/// lilak logger
class LKLogger
{
  public:
    LKLogger(TString name, const std::string &title ,int rank, int option);
    LKLogger(const std::string &title ,int line);

    template <class T> LKLogger &operator<<(const T &v)
    {
      if (LKLogManager::LogToConsol()) std::cout << v;
      if (LKLogManager::LogToFile()) LKLogManager::GetLogFile() << v;
      return *this;
    }

    LKLogger &operator<<(std::ostream&(*f)(std::ostream&))
    {
      if (LKLogManager::LogToConsol()) std::cout << *f;
      if (LKLogManager::LogToFile()) LKLogManager::GetLogFile() << *f;
      return *this;
    }
};

#endif
