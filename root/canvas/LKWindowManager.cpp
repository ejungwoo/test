#include "LKWindowManager.h"
#include <iostream>
using namespace std;

ClassImp(LKWindowManager);

LKWindowManager* LKWindowManager::fInstance = nullptr;

LKWindowManager* LKWindowManager::GetWindowManager() {
    if (fInstance == nullptr)
        fInstance = new LKWindowManager();
    return fInstance;
}

LKWindowManager::LKWindowManager()
{
    Init();
}

bool LKWindowManager::Init()
{
    // Put intialization todos here which are not iterative job though event
    e_info << "Initializing LKWindowManager" << std::endl;

    ConfigureDisplay();

    return true;
}

void LKWindowManager::Clear(Option_t *option)
{
    TObject::Clear(option);
    fWDisplay = -1;
    fHDisplay = -1;
    fDWFull = -1;
    fDHFull = -1;
    fDHBar = 0;
    fWCurrent = 0;
    fHCurrent = 0;
    fDWCanvas = 600;
    fDHCanvas = 450;
    fDWSpacing = 25;
    fDHSpacing = 25;
    fWGlobalScale = 1;
    fHGlobalScale = 1;
}

void LKWindowManager::Print(Option_t *option) const
{
    cout << "fWDisplay  " << fWDisplay  << endl;
    cout << "fHDisplay  " << fHDisplay  << endl;
    cout << "fDWFull    " << fDWFull  << endl;
    cout << "fDHFull    " << fDHFull  << endl;
    cout << "fDHBar     " << fDHBar  << endl;
    cout << "fWCurrent  " << fWCurrent  << endl;
    cout << "fHCurrent  " << fHCurrent  << endl;
    cout << "fDWCanvas  " << fDWCanvas  << endl;
    cout << "fDHCanvas  " << fDHCanvas  << endl;
    cout << "fDWSpacing " << fDWSpacing  << endl;
    cout << "fDHSpacing " << fDHSpacing  << endl;
}

void LKWindowManager::ConfigureDisplay()
{
    Drawable_t id = gClient->GetRoot()->GetId();
    gVirtualX -> GetWindowSize(id, fWDisplay, fHDisplay, fDWFull, fDHFull);
    fWCurrent = fDWFull*0.05;
    fHCurrent = fDHFull*0.1;
    cout << "Display position = (" << fWDisplay << ", " << fHDisplay << "), size = (" << fDWFull << ", " << fDHFull << ")" << endl;
}

TCanvas *LKWindowManager::CanvasR(const char *name, const char *title, Int_t ww, Int_t wh, Double_t rw, Double_t rh)
{
    return CanvasR(name, title, -1, -1, ww, wh, rw, rh);
}

TCanvas *LKWindowManager::CanvasR(const char *name, const char *title, Int_t w, Int_t h, Int_t ww, Int_t wh, Double_t rw, Double_t rh)
{
    if (w<0) {
        w = fWCurrent;
    }
    if (h<0) {
        h = fHCurrent;
    }

    if (ww<=0 && wh<=0) {
        ww = fDWCanvas;
        wh = fDHCanvas;
    }
    else if (ww<=0) {
        ww = wh * (double(fDWCanvas)/fDHCanvas);
    }
    else if (wh<=0) {
        wh = ww * (double(fDHCanvas)/fDWCanvas);
    }

    Int_t wFinal, hFinal;

    if (rw>0 && rh>0) {
        wFinal = rw * fDWFull;
        hFinal = rh * fDHFull;
    }
    else if (rw>0) {
        wFinal = rw * fDWFull;
        hFinal = wFinal * (double(wh)/ww);
    }
    else if (rh>0) {
        hFinal = rh * fDHFull;
        wFinal = hFinal * (double(ww)/wh);
    }

    wFinal = wFinal * fWGlobalScale;
    hFinal = hFinal * fHGlobalScale;

    //e_cout << "new TCanvas(\"" << name << "\", \"" << title << "\", " << w << ", " << h << ", " << wFinal << ", " << hFinal << ");" << endl;
    auto cvs = new TCanvas(name, title, w, h, wFinal, hFinal);

    fWCurrent = fWCurrent + fDWSpacing; 
    fHCurrent = fHCurrent + fDHSpacing; 

    return cvs;
}
