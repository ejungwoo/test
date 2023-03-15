#include "TROOT.h"
#include "TSystem.h"
#include "TDirectory.h"
#include "TApplication.h"
#include "LKParameterContainer.hh"
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <stdlib.h>
#include "TFormula.h"
#include "TObjString.h"

using namespace std;

ClassImp(LKParameterContainer)

LKParameterContainer::LKParameterContainer(Bool_t collect)
:TObjArray(), fCollectionMode(collect)
{
  fName = "ParameterContainer";
}

LKParameterContainer::LKParameterContainer(const char *parName, Bool_t collect)
:LKParameterContainer(collect)
{
  AddFile(TString(parName));
}

void LKParameterContainer::ProcessParNotFound(TString name, TString val) {
  if (fCollectionMode) {
    lk_warning << "parameter " << name << " does not exist!" << endl;
    lk_warning << "parameter will be added with default value." << endl;
    SetPar(name,val,"This parameter is collected from parameter collecting mode. Please modify the value");
  }
  else {
    lk_error << "parameter " << name << " does not exist!" << endl;
    gApplication -> Terminate();
  }
}

void LKParameterContainer::ProcessTypeError(TString name, TString value, TString type) const {
  lk_error << "parameter " << name << "=" << value << " is not convertable to " << type << endl;
  gApplication -> Terminate();
}

bool LKParameterContainer::CheckFormulaValidity(TString formula, bool isInt) const
{
  if (isInt && formula.Index(".")>=0)
    return false;

  TString formula2 = formula;
  formula2.ReplaceAll("+"," ");
  formula2.ReplaceAll("-"," ");
  formula2.ReplaceAll("/"," ");
  formula2.ReplaceAll("*"," ");
  formula2.ReplaceAll("."," ");

  if (!formula2.IsDigit())
    return false;

  return true;
}

double LKParameterContainer::Eval(TString formula) const
{
  return TFormula("formula",formula).Eval(0);
}

void LKParameterContainer::SaveAs(const char *fileName, Option_t *) const
{
  TString fileName0(fileName);
  if (fileName0.Index(".") < 0)
    fileName0 = fileName0 + ".par";
  Print(fileName0);
}

bool LKParameterContainer::IsEmpty() const
{
  if (GetEntries()>0)
    return false;
  return true;
}

void LKParameterContainer::ReplaceVariablesFast(TString &valInput, TString parName) const
{
  int ienv = valInput.Index("e{");
  while (ienv>=0) {
    int fenv = valInput.Index("}",1,ienv,TString::kExact);
    valInput.Replace(ienv,fenv-ienv+1,getenv(TString(valInput(ienv+2,fenv-ienv-2))));
    ienv = valInput.Index("e{");
  }

  int ipar = valInput.Index("{");
  while (ipar>=0) {
    int fpar = valInput.Index("}",1,ipar,TString::kExact);
    TString parName2 = valInput(ipar+1,fpar-ipar-1);
    if (parName2==parName || parName2.Index(parName+"[")>=0) {
      lk_error << "The parameter is refering to the valInput it self!" << endl;
      gApplication -> Terminate();
    }
    TString parValue2 = GetParStringFast(parName2);
    valInput.Replace(ipar,fpar-ipar+1,parValue2);
    ipar = valInput.Index("{");
  }

  if (valInput[0] == '$') {
    TString env = valInput;
    Ssiz_t nenv = env.First("/");
    env.Resize(nenv);
    valInput.Replace(0, nenv+1, getenv(env));
  }

  {
    valInput.ReplaceAll("kWhite"  ,"0");
    valInput.ReplaceAll("kBlack"  ,"1");
    valInput.ReplaceAll("kGray"   ,"920");
    valInput.ReplaceAll("kRed"    ,"632");
    valInput.ReplaceAll("kGreen"  ,"416");
    valInput.ReplaceAll("kBlue"   ,"600");
    valInput.ReplaceAll("kYellow" ,"400");
    valInput.ReplaceAll("kMagenta","616");
    valInput.ReplaceAll("kCyan"   ,"432");
    valInput.ReplaceAll("kOrange" ,"800");
    valInput.ReplaceAll("kSpring" ,"820");
    valInput.ReplaceAll("kTeal"   ,"840");
    valInput.ReplaceAll("kAzure"  ,"860");
    valInput.ReplaceAll("kViolet" ,"880");
    valInput.ReplaceAll("kPink"   ,"900");
  }

  if (CheckFormulaValidity(valInput)) {
    valInput = Form("%f",Eval(valInput));
    while (valInput.Index(".")>=0 && valInput.EndsWith("0") && valInput.Index(".")<valInput.Sizeof()-2) {
      valInput.Remove(valInput.Sizeof()-2,1);
    }
    if (valInput.EndsWith("."))
      valInput.Remove(valInput.Sizeof()-2,1);
  }
}

void LKParameterContainer::ReplaceVariables(TString &valInput, TString parName)
{
  int ienv = valInput.Index("e{");
  while (ienv>=0) {
    int fenv = valInput.Index("}",1,ienv,TString::kExact);
    valInput.Replace(ienv,fenv-ienv+1,getenv(TString(valInput(ienv+2,fenv-ienv-2))));
    ienv = valInput.Index("e{");
  }

  int ipar = valInput.Index("{");
  while (ipar>=0) {
    int fpar = valInput.Index("}",1,ipar,TString::kExact);
    TString parName2 = valInput(ipar+1,fpar-ipar-1);
    if (parName2==parName || parName2.Index(parName+"[")>=0) {
      lk_error << "The parameter is refering to the valInput it self!" << endl;
      gApplication -> Terminate();
    }
    TString parValue2 = GetParString(parName2);
    valInput.Replace(ipar,fpar-ipar+1,parValue2);
    ipar = valInput.Index("{");
  }

  if (valInput[0] == '$') {
    TString env = valInput;
    Ssiz_t nenv = env.First("/");
    env.Resize(nenv);
    env.Remove(0,1);
    valInput.Replace(0, nenv+1, getenv(env));
  }

}

Int_t LKParameterContainer::AddFile(TString fileName, bool addFilePar)
{
  ReplaceVariables(fileName);

  TString fileNameFull;

  bool existFile = false;

  if (fileName[0]=='/' || fileName[0]=='$' || fileName =='~'|| fileName[0]=='.') {
    fileNameFull = fileName;
    if (!TString(gSystem -> Which(".", fileNameFull.Data())).IsNull())
      existFile = true;
  }
  else
  {
    fileNameFull = TString(gSystem -> Getenv("PWD")) + "/" + fileName;
    if (!TString(gSystem -> Which(".", fileNameFull.Data())).IsNull())
      existFile = true;
    else
    {
      fileNameFull = TString(gSystem -> Getenv("NEST_PATH")) + "/input/" + fileName;
      if (!TString(gSystem -> Which(".", fileNameFull.Data())).IsNull())
        existFile = true;
    }
  }

  if (!existFile) {
    lk_error << "Parameter file " << fileNameFull << " does not exist!" << endl;
    return 0;
  }

  fileNameFull.ReplaceAll("//","/");

  lk_info << "Adding parameter file " << fileNameFull << endl;

  TString parName = Form("INPUT_FILE_%d", fNumInputFiles);
  TString parName2 = Form("<<%d", fNumInputFiles);

  fNumInputFiles++;
  if (addFilePar)
    SetPar(parName, fileNameFull);
  else {
    SetPar("","",TString("# ") + parName2 + " " + fileNameFull);
  }

  ifstream file(fileNameFull);
  string line;

  Int_t countParameters = 0;
  while (getline(file, line)) {
    if (SetPar(line))
      countParameters++;
  }

  if (countParameters == 0) {
    this -> Remove(FindObject(parName));
    fNumInputFiles--;
  }

  parName.Replace(0,11,"<<");
  SetPar("","", Form("%s %d parameters where added",parName.Data(),countParameters));

  return countParameters;
}

Int_t LKParameterContainer::AddParameterContainer(LKParameterContainer *parc)
{
  lk_info << "Adding parameter container " << parc -> GetName() << endl;

  TString parName = Form("INPUT_PARC_%d", fNumInputFiles);
  fNumInputFiles++;
  SetPar(parName, ""); //@todo

  Int_t countParameters = 0;
  Int_t countSameParameters = 0;

  TIter iterator(parc);
  TObject *obj;
  while ((obj = dynamic_cast<TObject*>(iterator())))
  {
    TString name = obj -> GetName();

    TObject *found = FindObject(name);
    if (found != nullptr) {
      if (name.Index("INPUT_FILE_")==0)
        ((TNamed *) obj) -> SetName(name+"_");
      else {
        lk_error << "Parameter " << name << " already exist!" << endl;
        ++countSameParameters ;
        continue;
      }
    }

    Add(obj);
    ++countParameters;
  }

  if (countParameters == 0) {
    this -> Remove(FindObject(parName));
    fNumInputFiles--;
  }

  return countParameters;
}

void LKParameterContainer::Print(Option_t *option) const
{
  TString printOptions(option);

  if (printOptions.Index("raw")>=0) {
    TObjArray::Print();
    return;
  }

  bool evalulatePar = false;
  bool showHiddenPar = false;
  bool showLineComments = false;
  bool showParComments = false;
  bool printToScreen = true;
  bool printToFile = false;
  ofstream fileOut;

  printOptions.ReplaceAll(":"," ");
  if (printOptions.Index("eval" )>=0) { evalulatePar = true;     printOptions.ReplaceAll("eval", ""); }
  if (printOptions.Index("line#")>=0) { showLineComments = true; printOptions.ReplaceAll("line#",""); }
  if (printOptions.Index("par#" )>=0) { showParComments = true;  printOptions.ReplaceAll("par#", ""); }
  if (printOptions.Index("all"  )>=0) { showHiddenPar = true;    printOptions.ReplaceAll("all",  ""); }
  printOptions.ReplaceAll(" ","");

  TString fileName = printOptions;
  if (fileName.IsNull()) {
    printToScreen = true;
  }
  else if (fileName.Index(".")>0) {
    printToFile = true;
    printToScreen = false;
  }

  if (printToScreen) {
    lx_cout << endl;
    lk_info << "Parameter Container" << endl;
  }

  if (printToFile)
  {
    lk_info << "Writting " << fileName << endl;
    fileOut.open(fileName);
    fileOut << "# " << fileName << " created from LKParameterContainer::Print" << endl;
    fileOut << endl;
  }

  TIter iterator(this);
  TNamed *obj;
  while ((obj = dynamic_cast<TNamed*>(iterator())))
  {
    TString parName = obj -> GetName();

    TString parValues = obj -> GetTitle();
    if (evalulatePar) {
      auto parN = GetParN(parName);
      if (parN==1)
        ReplaceVariablesFast(parValues,parName);
      else {
        parValues = "";
        for (auto iPar=0; iPar<parN; ++iPar) {
          TString parValue = GetParStringFast(parName,iPar);
          if (iPar==0) parValues = parValue;
          else parValues = parValues + " " + parValue;
        }
      }
    }

    TString parComment;
    if (!showHiddenPar)
      if (parName.Index("NUM_VALUES_")==0||parName.Index("COMMELK_PAR_")==0||parName.EndsWith("]"))
        continue;

    if (parName.Index("COMMELK_LINE_")>=0) {
      if (!showLineComments)
        continue;
      parName = parValues;
      parValues = "";
      if (parName[0]!='#')
        parName = TString("# ") + parName;
    }
    else if (parName.Index("INPUT_FILE_")>=0)
      parName.Replace(0,11,"<<");
    else if (parName.Index("INPUT_PARC_")>=0) {
      if (!showLineComments)
        continue;
      parName.Replace(0,11,"# Parameter container was added here; ");
    }
    else if (showParComments) {
      TNamed* objc = (TNamed *) FindObject(Form("COMMELK_PAR_%s",parName.Data()));
      if (objc!=nullptr)
        parComment = objc -> GetTitle();
      if (!parComment.IsNull()&&parComment[0]!='#')
        parComment = TString("# ") + parComment;
    }

    ostringstream ssLine;
    if (parName.Sizeof()>40)
      ssLine << parName << " " << parValues << " " << parComment << endl;
    else if (parName.Sizeof()>30)
      ssLine << left << setw(40) << parName << " " << parValues << " " << parComment << endl;
    else if (parName.Sizeof()>20)
      ssLine << left << setw(30) << parName << " " << parValues << " " << parComment << endl;
    else
      ssLine << left << setw(20) << parName << " " << parValues << " " << parComment << endl;

    if (printToScreen)
      lk_cout << ssLine.str();
    if (printToFile)
      fileOut << ssLine.str();
  }

  if (printToFile) {
    fileOut << endl;
  }
}

Bool_t LKParameterContainer::SetPar(std::string line)
{
  if (line.empty())
    return false;

  if (line.find("#") == 0) {
    SetPar("", "", TString(line));
    return true;
  }

  istringstream ss(line);
  TString parName;
  ss >> parName;

  TString parValues = line;
  parValues.Remove(0,parName.Sizeof()-1);
  while (parValues[0]==' ')
    parValues.Remove(0,1);

  int icomment = parValues.Index("#");
  TString parComment = parValues(icomment,parValues.Sizeof());

  if (icomment>0) {
    parValues = parValues(0,icomment);
    while (parValues[parValues.Sizeof()-2]==' ')
      parValues.Remove(parValues.Sizeof()-2,1);
  }

  if (parName.Index("<<")==0) {
    AddFile(parValues);
  }
  else {
    auto valueTokens = parValues.Tokenize(" ");
    Int_t numValues = valueTokens -> GetEntries();
    SetPar(parName, parValues, parComment);
    SetPar(TString("NUM_VALUES_")+parName,numValues);
    if (numValues>1) {
      for (auto iVal=0; iVal<numValues; ++iVal) {
        TString parValue(((TObjString *) valueTokens->At(iVal))->GetString());
        SetPar(parName+"["+iVal+"]",parValue);
      }
    }
  }

  return true;
}

Bool_t LKParameterContainer::SetPar(TString name, TString val, TString comment)
{
  if (FindObject(name) != nullptr) {
    lk_error << "Parameter " << name << " already exist!" << endl;
    return false;
  }

  if (name.IsNull()&&val.IsNull()&&!comment.IsNull())
    Add(new TNamed(TString(Form("COMMELK_LINE_%d",GetEntries())), comment));
  else {
    Add(new TNamed(name, val));
    if (!comment.IsNull())
      Add(new TNamed(TString(Form("COMMELK_PAR_%s",name.Data())), comment));
  }
  return true;
}

TString LKParameterContainer::GetParStringFast(TString name, Int_t idx) const
{
  if (idx>=0) return GetParStringFast(name+"["+idx+"]");

  TObject *obj = FindObject(name);
  TString value = ((TNamed *) obj) -> GetTitle();
  ReplaceVariablesFast(value,name);

  return value;
}

TString LKParameterContainer::GetParString(TString name, Int_t idx)
{
  if (idx>=0) return GetParString(name+"["+idx+"]");

  TObject *obj = FindObject(name);
  if (obj == nullptr) {
    ProcessParNotFound(name,"default_parameter_value");
    return "default_parameter_value";
  }

  TString value = ((TNamed *) obj) -> GetTitle();
  ReplaceVariables(value,name);

  return value;
}

Int_t LKParameterContainer::GetParN(TString name) const
{
  TString name_n = TString("NUM_VALUES_") + name;

  TObject *obj = FindObject(name_n);
  if (obj == nullptr) {
    if (FindObject(name)==nullptr)
      return 0;
    else
      return 1;
  }

  TString value = ((TNamed *) obj) -> GetTitle();

  return value.Atoi();
}

Bool_t LKParameterContainer::GetParBool(TString name, Int_t idx)
{
  if (idx>=0) return GetParBool(name+"["+idx+"]");

  TObject *obj = FindObject(name);
  if (obj == nullptr) {
    ProcessParNotFound(name,"false");
    return false;
  }

  TString value = ((TNamed *) obj) -> GetTitle();
  ReplaceVariables(value,name);

  value.ToLower();
       if (value=="true "||value=="1") return true;
  else if (value=="false"||value=="0") return false;
  else 
    ProcessTypeError(name,value,"bool");

  return true;
}

Int_t LKParameterContainer::GetParInt(TString name, Int_t idx)
{
  if (idx>=0) return GetParInt(name+"["+idx+"]");

  TObject *obj = FindObject(name);
  if (obj == nullptr) {
    ProcessParNotFound(name,"0");
    return 0;
  }

  TString value = ((TNamed *) obj) -> GetTitle();
  ReplaceVariables(value,name);

  if (!CheckFormulaValidity(value,1))
    ProcessTypeError(name, value, "int");

  return Int_t(Eval(value));
}

Double_t LKParameterContainer::GetParDouble(TString name, Int_t idx)
{
  if (idx>=0) return GetParDouble(name+"["+idx+"]");

  TObject *obj = FindObject(name);
  if (obj == nullptr) {
    ProcessParNotFound(name,"0.1");
    return 0.1;
  }

  TString value = ((TNamed *) obj) -> GetTitle();
  ReplaceVariables(value,name);

  if (!CheckFormulaValidity(value))
    ProcessTypeError(name, value, "double");

  return Eval(value);
}

TVector3 LKParameterContainer::GetParV3(TString name)
{
  TString xname = name + "[0]";
  TString yname = name + "[1]";
  TString zname = name + "[2]";

  TObject *xobj = FindObject(xname);
  if (xobj == nullptr) {
    ProcessParNotFound(name,".9,.9,.9");
    return TVector3(.9,.9,.9);
  }

  double x = GetParDouble(xname);
  double y = GetParDouble(yname);
  double z = GetParDouble(zname);

  return TVector3(x,y,z);
}

Int_t LKParameterContainer::GetParColor(TString name, Int_t idx)
{
  if (idx>=0) return GetParColor(name+"["+idx+"]");

  TObject *obj = FindObject(name);
  if (obj == nullptr) {
    ProcessParNotFound(name,"kBlack");
    return 1;//"kBlack";
  }

  TString value = ((TNamed *) obj) -> GetTitle();
  ReplaceVariables(value,name);

  if (value.Index("k")==0)
  {
    value.ReplaceAll("kWhite"  ,"0");
    value.ReplaceAll("kBlack"  ,"1");
    value.ReplaceAll("kGray"   ,"920");
    value.ReplaceAll("kRed"    ,"632");
    value.ReplaceAll("kGreen"  ,"416");
    value.ReplaceAll("kBlue"   ,"600");
    value.ReplaceAll("kYellow" ,"400");
    value.ReplaceAll("kMagenta","616");
    value.ReplaceAll("kCyan"   ,"432");
    value.ReplaceAll("kOrange" ,"800");
    value.ReplaceAll("kSpring" ,"820");
    value.ReplaceAll("kTeal"   ,"840");
    value.ReplaceAll("kAzure"  ,"860");
    value.ReplaceAll("kViolet" ,"880");
    value.ReplaceAll("kPink"   ,"900");
  }

  if (!CheckFormulaValidity(value,1))
    ProcessTypeError(name,value,"color");

  return Int_t(Eval(value));
}

std::vector<bool> LKParameterContainer::GetParVBool(TString name)
{
  std::vector<bool> array;
  auto npar = GetParN(name);
  for (auto i=0; i<npar; ++i)
    array.push_back(GetParBool(name,i));
  return array;
}

std::vector<int> LKParameterContainer::GetParVInt(TString name)
{
  std::vector<int> array;
  auto npar = GetParN(name);
  for (auto i=0; i<npar; ++i)
    array.push_back(GetParInt(name,i));
  return array;
}

std::vector<double> LKParameterContainer::GetParVDouble(TString name)
{
  std::vector<double> array;
  auto npar = GetParN(name);
  for (auto i=0; i<npar; ++i)
    array.push_back(GetParDouble(name,i));
  return array;
}

std::vector<TString> LKParameterContainer::GetParVString(TString name)
{
  std::vector<TString> array;
  auto npar = GetParN(name);
  for (auto i=0; i<npar; ++i)
    array.push_back(GetParString(name,i));
  return array;
}

Bool_t LKParameterContainer::CheckPar(TString name) const
{
  if (FindObject(name) != nullptr) return true;
  return false;
}
