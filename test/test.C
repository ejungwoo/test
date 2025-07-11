void test()
{
    LKParameterContainer par("ha.par");
    par.Print();
    TVector3 a;
    par.UpdatePar(a,"value");
    a.Print();
}
