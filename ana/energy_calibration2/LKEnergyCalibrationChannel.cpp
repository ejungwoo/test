#include "LKEnergyCalibrationChannel.h"

LKEnergyCalibrationChannel::LKEnergyCalibrationChannel()
{
}

void LKEnergyCalibrationChannel::AddEnergy(Energy)
{
    if (!IsPositionSensitiveStrip(channel))
    {
        auto energy = channel -> GetEnergy();
        if (calibration==1) CalibrateC0(det,side,strip,energy);
        fHistEnergy[det][side][strip] -> Fill(energy);
        fHistEnergyDetector[side] -> Fill(det*(side==0?fNumJStrips:fNumOStrips)+strip,energy);
    }
    else
    {
        auto energyR = channel -> GetEnergy();
        auto energyL = channel -> GetEnergy2();
        if (energyL<0)
            continue;
        if (calibration==1)
        {
            CalibrateC1(det,side,strip,0,energyL);
            CalibrateC1(det,side,strip,1,energyR);
            if (GetNumOhmicStrips(det)>1)
            {
                CalibrateCE(det,side,strip,0,energyL);
                CalibrateCE(det,side,strip,1,energyR);
            }
        }
        auto sum = energyR + energyL;
        auto pos = (energyR - energyL) / sum;
        fHistEnergyDetector[side] -> Fill(det*(side==0?fNumJStrips:fNumOStrips)+strip,sum);
        fHistEnergySum[det][side][strip] -> Fill(sum);
        fHistEnergyPosition[det][side][strip] -> Fill(pos,sum);
        if (calibration==0) fHistLeftRight[det][side][strip] -> Fill(energyR, energyL);
        if (0)//calibration==1)
        {
            for (auto gate=0; gate<fNumGates; ++gate) {
                double range1 = eGateRange[gate][0];
                double range2 = eGateRange[gate][1];
                if (sum>range1 && sum<range2) {
                    fHistLeftRightGate     [det][side][strip][gate] -> Fill(energyR, energyL);
                    fHistEnergyPositionGate[det][side][strip][gate] -> Fill(pos,sum);
                }
            }
        }
    }
}
