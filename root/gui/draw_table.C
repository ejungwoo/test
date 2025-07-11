#include <TApplication.h>
#include <TGClient.h>
#include <TGFrame.h>
#include <TGTable.h>
#include <TVirtualTableInterface.h>
#include <TString.h>
#include <vector>

#include "LKStringTableInterface.cpp"

void draw_table()
{
    auto fTableInterface = new LKStringTableInterface(10, 5);
    fTableInterface->ReadParameterContainer(new LKParameterContainer("config_test.mac"));

    TGMainFrame *main = new TGMainFrame(gClient->GetRoot(), 800, 600);

    TGCompositeFrame *container = new TGCompositeFrame(main, 800, 600, kSunkenFrame | kDoubleBorder);
    TGCanvas *canvas = new TGCanvas(container, 800, 600);

    TGTable *table = new TGTable(canvas->GetViewPort(), 0, fTableInterface);

    table->SetEditable(kTRUE);

    // (new) 각 column 폭 넓히기
    //for (int c = 0; c < fTableInterface->GetNColumns(); ++c) table->SetColumnWidth(c, 200); // or 300, 너 상황에 맞게!

    canvas->SetContainer(table);
    container->AddFrame(canvas);
    main->AddFrame(container, new TGLayoutHints(kLHintsExpandX | kLHintsExpandY));

    main->SetWindowName("Editable String Table (with scroll)");
    main->MapSubwindows();
    main->Resize();
    main->MapWindow();
}
