#ifndef LKENERGYCALIBRATION_HH
#define LKENERGYCALIBRATION_HH

#include "TObjArray.h"
#include <tuple>
#include <map>

#include "LKEnergyCalibrationChannel.h"

class LKEnergyCalibration : public TObjArray
{
    public:
        LKEnergyCalibration() {}
        int AddDetector(TString detName="CSD");
        //int AddChannel(int det, int side=-1, int strip=-1);
        //int AddEnergy(int id, double energy);
        //int AddChannelR(int det, int side=-1, int strip=-1);
        //int AddEnergyR(int id, double energyL, energyR);

        int FindChannelID(int det, int side=-1, int strip=-1);

    private:
        std::map<std::tuple<int, int, int>, int> fChannelMap;
        int fCountDetectors = 0;
        int fCountChannels = 0;
};

#endif
