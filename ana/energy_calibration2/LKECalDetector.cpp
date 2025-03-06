#include "LKECalDetector.h"

void LKECalDetector::SetNumSides(int num_sides)
{
    fNumSides = num_sides;
    for (auto iSide=0; iSide<fNumSides; ++iSide)
    {
        fChannel = new LKECalChannel**[fNumSides]
    }
    fNumStrips = new int[fNumChan];
    fNumReadouts = new int[fNumChan];
}

void LKECalDetector::SetSide(int side, int num_strips, bool resistive_strip=false)
{
    fNumStrips[side] = num_strips;
    fNumReadouts[side] = (resistive_strip?2:1);

    fChannel[side] = new LKECalChannel*[num_strips]
    for (auto strip=0; strip<num_strips; ++strip)
    {
        auto channel = fChannel[side][strip];
        channel -> SetResistiveStrip(resistive_strip);
    }
}

int LKECalDetector::GetNumChannels()
{
}
