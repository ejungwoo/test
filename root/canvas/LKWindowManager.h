#ifndef LKWINDOWMANAGER_HH
#define LKWINDOWMANAGER_HH

#include "TObject.h"
#include "LKLogger.h"
#include "TCanvas.h"

#define lk_wman             LKWindowManager::GetWindowManager()
#define lk_canvas(name)     LKWindowManager::GetWindowManager() -> Canvas(name)
#define lk_draw(pad,object) LKWindowManager::GetWindowManager() -> Draw(pad,object)

class LKWindowManager : public TObject
{
    public:
        LKWindowManager();
        virtual ~LKWindowManager() { ; }
        static LKWindowManager* GetWindowManager();

        bool Init();
        void Clear(Option_t *option="");
        void Print(Option_t *option="") const;

        Int_t  GetWDisplay() const  { return fWDisplay; }
        Int_t  GetHDisplay() const  { return fHDisplay; }
        UInt_t GetDWFull() const  { return fDWFull; }
        UInt_t GetDHFull() const  { return fDHFull; }

        void SetDHBar(UInt_t hBar) {
            fDHBar = hBar;
            if (fHCurrent==0)
                fHCurrent = hBar;
        }

        void SetDWCanvas(UInt_t wCanvas) { fDWCanvas = wCanvas; }
        void SetDHCanvas(UInt_t hCanvas) { fDHCanvas = hCanvas; }
        void SetDWSpacing(UInt_t dwCanvas) { fDWSpacing = dwCanvas; }
        void SetDHSpacing(UInt_t dhCanvas) { fDHSpacing = dhCanvas; }

        void SetGlobalScale(Double_t xScale, Double_t yScale) {
            fWGlobalScale = xScale;
            fHGlobalScale = yScale;
        }

        TCanvas *Canvas  (const char *name)                  { return CanvasR(name, name, 0, 0, 0,  0.5); }
        TCanvas *CanvasRH(const char *name, Double_t rh=0.5) { return CanvasR(name, name, 0, 0, 0,  rh); }
        TCanvas *CanvasRW(const char *name, Double_t rw=0.4) { return CanvasR(name, name, 0, 0, rw, 0); }
        TCanvas *CanvasR (const char *name, const char *title, Int_t ww, Int_t wh, Double_t rw, Double_t rh);

        /**
         * @param w
         *      - w(x) position of the canvas in the display 
         * @param h
         *      - h(y) position of the canvas in the display 
         * @param ww
         *      - width of the canvas
         * @param wh
         *      - height of the canvas
         * @param rw
         *      - Ratio of canvas width relative to the full display size
         *      - If rw>0 and rh<=0, canvas size is (rw*fDWFull, rw*fDWFull*ww/wh)
         *      (fDWFull and fDHFull is the width and height of the current display)
         *      - If both rw and rh are >0, canvas size is (rw*fDWFull, rh*fDHFull)
         * @param rh
         *      - Ratio of canvas height relative to the full display size
         *      - If rw<=0 and rh>0, canvas size is (rh*fDHFull, rh*fDHFull*wh/ww)
         *      (fDWFull and fDHFull is the width and height of the current display)
         *      - If both rw and rh are >0, canvas size is (rw*fDWFull, rh*fDHFull)
         */
        TCanvas *CanvasR(const char *name, const char *title, Int_t w, Int_t h, Int_t ww, Int_t wh, Double_t rw, Double_t rh);

    private:
        void ConfigureDisplay();

    private:
        static LKWindowManager* fInstance;

        Int_t        fWDisplay = -1; /// relative width  position of current display from main display
        Int_t        fHDisplay = -1; /// relative height position of current display from main display

        UInt_t       fDWFull = 0; /// width  of current display
        UInt_t       fDHFull = 0; /// height of current display

        Int_t        fDHBar = 0; /// height of the top bar

        Int_t        fWCurrent = 0;  /// width  position of next canvas
        Int_t        fHCurrent = 0;  /// height position of next canvas

        Int_t        fDWCanvas = 600; /// default width  of canvas
        Int_t        fDHCanvas = 450; /// default height of canvas

        Int_t        fDWSpacing = 25; /// default width  spacing of canvas
        Int_t        fDHSpacing = 25; /// default height spacing of canvas

        Double_t     fWGlobalScale = 1; /// default width  spacing of canvas
        Double_t     fHGlobalScale = 1; /// default height spacing of canvas

    ClassDef(LKWindowManager,1);
};

#endif
