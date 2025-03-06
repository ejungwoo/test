#include "json.h"
#include "jsoncpp.cpp"

void test()
{
  Json::Value config;
  ifstream fileConf("config_test.json");
  fileConf >> config;

  string sreadtype = config["ReadType"].asString();
  int readtype = atoi(sreadtype.c_str());
  string snumfiles = config["NumberofFiles"].asString();
  int numfiles = atoi(snumfiles.c_str());
  cout << readtype << " " << numfiles << endl;

  //string watcherIP = config["watcherIP"].asString();
  //string swatcherPort = config["watcherPort"].asString();
  //string sConverterPort = config["ConverterPort"].asString();
  //string sCoBoServerPort = config["CoBoServerPort"].asString();
  //string sMutantServerPort = config["MutantServerPort"].asString();
  //int watcherPort = atoi(swatcherPort.c_str());
  //int converterPort = atoi(sConverterPort.c_str());
  //int CoBoServerPort = atoi(sCoBoServerPort.c_str());
  //int MutantServerPort = atoi(sMutantServerPort.c_str());
  //string sBucketSize = config["BucketSize"].asString();
  //int BucketSize = atoi(sBucketSize.c_str());
  //string mapChanToMM = config["ChanToMMMapFileName"].asString();
  //string mapChanToSi = config["ChanToSiMapFileName"].asString();
  //string sRootConvert = config["RootConvertEnable"].asString();
  //string sEnergyMethod = config["EnergyFindingMethod"].asString();
  //int energymethod = atoi(sEnergyMethod.c_str());
  //string sReadRW = config["ReadResponseWaveformFlag"].asString();
  //int readrw = atoi(sReadRW.c_str());
  //string rwfilename = config["ResponseWaveformFileName"].asString();
  //int RootConvert = atoi(sRootConvert.c_str());
  //string sScalerMode = config["ScalerMode"].asString();
  //int ScalerMode = atoi(sScalerMode.c_str());
  //string sd2pMode = config["2pMode"].asString();
  //int d2pMode = atoi(sd2pMode.c_str());
  //string supdatefast = config["UpdateFast"].asString();
  //int updatefast = atoi(supdatefast.c_str());
  string sIgnoreMM = config["IgnoreMicromegas"].asString();
  int IgnoreMM = atoi(sIgnoreMM.c_str());
  cout << IgnoreMM << endl;
  //int IgnoreMM = 1;
  //string sDrawWaveform = config["DrawWaveformEnable"].asString();
  //int DrawWaveform = atoi(sDrawWaveform.c_str());
  //string sCleanTrack = config["CleanTrackEnable"].asString();
  //int cleantrack = atoi(sCleanTrack.c_str());
  //string sDrawTrack = config["DrawTrackEnable"].asString();
  //int DrawTrack = atoi(sDrawTrack.c_str());
  //string sSkipEvents = config["SkipEvents"].asString();
  //int SkipEvents = atoi(sSkipEvents.c_str());
  //string sfirstEventNo = config["firstEventNo"].asString();
  //int firstEventNo=0;
  //string goodEventList;
  //if(SkipEvents==1) firstEventNo = atoi(sfirstEventNo.c_str());
  //if(SkipEvents==2) goodEventList = config["firstEventNo"].asString();
  //return 0;
}
