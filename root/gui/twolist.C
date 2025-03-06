#include <TApplication.h>
#include <TGClient.h>
#include <TGFrame.h>
#include <TGListBox.h>
//#include <TGTextButton.h>
#include <iostream>
#include <vector>

class ClassSelectionGUI : public TGMainFrame {
private:
    TGListBox *allClassesList;
    TGListBox *selectedClassesList;
    TGTextButton *moveButton;
    TGTextButton *removeButton;
    
    std::vector<std::string> selectedClassNames;  // Track selected class names

public:
    ClassSelectionGUI(const TGWindow *p, UInt_t w, UInt_t h);
    virtual ~ClassSelectionGUI();

    void MoveSelectedClass();  // Move from allClassesList to selectedClassesList
    void RemoveSelectedClass(); // Remove from selectedClassesList
};

ClassSelectionGUI::ClassSelectionGUI(const TGWindow *p, UInt_t w, UInt_t h)
    : TGMainFrame(p, w, h) {

    // Main horizontal layout
    TGHorizontalFrame *mainFrame = new TGHorizontalFrame(this, w, h);

    // Left list (All classes)
    allClassesList = new TGListBox(mainFrame);
    mainFrame->AddFrame(allClassesList, new TGLayoutHints(kLHintsExpandX | kLHintsExpandY, 5, 5, 5, 5));

    // Add some sample class names
    const char *classNames[] = {"ClassA", "ClassB", "ClassC", "ClassD", "ClassE"};
    for (int i = 0; i < 5; i++) {
        allClassesList->AddEntry(classNames[i], i + 1);
    }
    allClassesList->Resize(100, 200);
    allClassesList->MapSubwindows();

    // Button frame (Holds move and remove buttons)
    TGVerticalFrame *buttonFrame = new TGVerticalFrame(mainFrame);

    // Move button (→)
    moveButton = new TGTextButton(buttonFrame, "→");
    moveButton->Connect("Clicked()", "ClassSelectionGUI", this, "MoveSelectedClass()");
    buttonFrame->AddFrame(moveButton, new TGLayoutHints(kLHintsCenterX | kLHintsExpandY, 5, 5, 5, 5));

    // Remove button (←)
    removeButton = new TGTextButton(buttonFrame, "←");
    removeButton->Connect("Clicked()", "ClassSelectionGUI", this, "RemoveSelectedClass()");
    buttonFrame->AddFrame(removeButton, new TGLayoutHints(kLHintsCenterX | kLHintsExpandY, 5, 5, 5, 5));

    mainFrame->AddFrame(buttonFrame);

    // Right list (Selected classes)
    selectedClassesList = new TGListBox(mainFrame);
    mainFrame->AddFrame(selectedClassesList, new TGLayoutHints(kLHintsExpandX | kLHintsExpandY, 5, 5, 5, 5));

    // Add main frame to window
    AddFrame(mainFrame, new TGLayoutHints(kLHintsExpandX | kLHintsExpandY));

    // Final setup
    SetWindowName("Class Selection GUI");
    MapSubwindows();
    Resize(GetDefaultSize());
    MapWindow();
}

ClassSelectionGUI::~ClassSelectionGUI() {
    Cleanup();
}

// Function to move selected class
void ClassSelectionGUI::MoveSelectedClass() {
    Int_t selectedId = allClassesList->GetSelected();
    TGTextLBEntry *selectedEntry = (TGTextLBEntry *)allClassesList->GetEntry(selectedId);

    if (selectedEntry) {
        std::string selectedClass = selectedEntry->GetText()->GetString();

        // Check if class is already in the selected list
        if (std::find(selectedClassNames.begin(), selectedClassNames.end(), selectedClass) != selectedClassNames.end()) {
            std::cout << "Class already selected: " << selectedClass << std::endl;
            return;
        }

        // Add to the selected list
        selectedClassesList->AddEntry(selectedClass.c_str(), selectedId);
        selectedClassNames.push_back(selectedClass);

        selectedClassesList->MapSubwindows();
        selectedClassesList->Layout();
    }
}

// Function to remove selected class from right list
void ClassSelectionGUI::RemoveSelectedClass() {
    Int_t selectedId = selectedClassesList->GetSelected();
    TGTextLBEntry *selectedEntry = (TGTextLBEntry *)selectedClassesList->GetEntry(selectedId);

    if (selectedEntry) {
        std::string selectedClass = selectedEntry->GetText()->GetString();

        // Remove from tracking vector
        selectedClassNames.erase(std::remove(selectedClassNames.begin(), selectedClassNames.end(), selectedClass), selectedClassNames.end());

        // Remove from GUI
        selectedClassesList->RemoveEntry(selectedId);
        selectedClassesList->MapSubwindows();
        selectedClassesList->Layout();
    }
}

// Run the application
void RunClassSelection() {
    TApplication app("ClassSelection", nullptr, nullptr);
    new ClassSelectionGUI(gClient->GetRoot(), 400, 300);
    app.Run();
}

void twolist() {
    RunClassSelection();
}
