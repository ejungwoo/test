#ifndef LKECALDETECTOR_HH
#define LKECALDETECTOR_HH

#include "TObjArray.h"
#include <tuple>
#include <map>

#include "LKECalChannel.h"

class LKECalDetector
{
    public:
        LKECalDetector() {}
        void SetNumSides(int num_sides) { fNumSides = num_sides; }
        void SetSide(int side, int num_strips, bool resistive_strip=false);
        int GetNumChannels();

    private:
        LKECalChannel*** fChannel;
        int fNumSides = 0;
        int *fNumStrips;
        int *fNumReadouts;
};

#endif
