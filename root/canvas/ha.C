#include "LKWindowManager.cpp"
#include "LKWindowManager.h"

void ha()
{
    lk_wman -> CanvasR("c0","c0",0,0,-1,-1,1,0.2);

    lk_canvas("c1");
    auto hist = new TH2D("hist","t;x;y;z;",100,-40,40,100,0,100);
    hist -> Draw();
}
