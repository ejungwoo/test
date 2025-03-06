#include <TApplication.h>
#include <TGClient.h>
#include <TGFrame.h>
#include <TGNumberEntry.h>
#include <TGLayout.h>

class InteractiveTable : public TGMainFrame {
private:
    static const int nRows = 5;
    static const int nCols = 4;
    TGNumberEntry *entries[nRows][nCols]; // Store entries for easy access

public:
    InteractiveTable(const TGWindow *p, UInt_t w, UInt_t h);
    virtual ~InteractiveTable();
};

InteractiveTable::InteractiveTable(const TGWindow *p, UInt_t w, UInt_t h) 
    : TGMainFrame(p, w, h) {

    // Create a composite frame for the table
    TGCompositeFrame *tableFrame = new TGCompositeFrame(this, w, h, kVerticalFrame);
    
    // Use a matrix layout to arrange number entries in a grid
    TGMatrixLayout *layout = new TGMatrixLayout(tableFrame, nRows, nCols, 10, 10);
    tableFrame->SetLayoutManager(layout);

    // Populate the table with TGNumberEntry widgets
    for (int i = 0; i < nRows; i++) {
        for (int j = 0; j < nCols; j++) {
            entries[i][j] = new TGNumberEntry(tableFrame, (i + 1) * 10 + j, 6);
            tableFrame->AddFrame(entries[i][j], new TGLayoutHints(kLHintsExpandX | kLHintsExpandY, 2, 2, 2, 2));
        }
    }

    // Add table frame to the main frame
    AddFrame(tableFrame, new TGLayoutHints(kLHintsExpandX | kLHintsExpandY));

    // Set window properties
    SetWindowName("Interactive Table");
    MapSubwindows();
    Resize(GetDefaultSize());
    MapWindow();
}

InteractiveTable::~InteractiveTable() {
    Cleanup();
}

void RunInteractiveTable() {
    TApplication app("ROOT Interactive Table", nullptr, nullptr);
    new InteractiveTable(gClient->GetRoot(), 400, 300);
    app.Run();
}

//int main(int argc, char **argv) {
int ha() {
    RunInteractiveTable();
    return 0;
}

