#include "LKEnergyCalibration.h"

//int LKEnergyCalibration::AddChannel(int det, int side, int strip)
//{
//    fChannelMap[std::make_tuple(det, side, strip)] = fCountChannels;
//    fCountChannels++;
//    return fCountChannels;
//}
//
//int LKEnergyCalibration::FindChannelID(int det, int side, int strip)
//{
//    std::tuple<int, int, int> key = std::make_tuple(1, 2, 3);
//    if (fChannelMap.find(key) != fChannelMap.end())
//        return fChannelMap[key];
//    return -1;
//}

int LKEnergyCalibration::AddDetector(TString detName)
{
    LKParameterContainer par(TString("ecal.")+detName+".mac");
    auto num_side = par.GetParInt("num_sides");

    auto detector = new LKECalDetector(fCountDetectors++);
    detector -> SetNumSides(num_sides);

    for (auto side=0; side<num_side; ++side)
    {
        int num_strips = 1;
        bool resistive_strip = false;
        par.UpdatePar(num_strips,Form("side%d/num_strips",side));
        par.UpdatePar(resistive_strip,Form("side%d/resistive_strip",side));

        detector -> SetSide(side, num_strips, resistive_strip);
    }

    fCountChannels += detector -> GetNumChannels();
}
