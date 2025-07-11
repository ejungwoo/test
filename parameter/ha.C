void ha()
{
    auto par = new LKParameterContainer("test.par");
    //par -> Print();
    //par -> CreateGroupContainer("NPTool/Reaction") -> Print();
    //par -> CreateGroupContainer("NPTool/Reaction/Beam") -> Print();
    //par -> FindPar("Particle") -> Print();
    par -> FindPar("NPTool/Reaction/Beam/Particle") -> Print();
    cout << par -> FindPar("NPTool/Reaction/Beam/Particle") -> GetGroup() << endl;
    cout << par -> FindPar("NPTool/Reaction/Beam/Particle") -> GetGroup(0) << endl;
    cout << par -> FindPar("NPTool/Reaction/Beam/Particle") -> GetGroup(1) << endl;
    cout << par -> FindPar("NPTool/Reaction/Beam/Particle") -> GetGroup(2) << endl;
    //NPTool/Reaction/Beam/Particle           proton
}
