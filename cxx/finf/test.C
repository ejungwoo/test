void print(bool (*fisout)(TVector3 pos))
{
    if (fisout(TVector3(0,0,10)))
        cout << "out!" << endl;
    else
        cout << "in!" << endl;
}

//bool fisout(TVector3 pos)
//{
//    if (pos.Z()>1)
//        return true;
//    return false;
//}

void test()
{
    auto fisout = [](TVector3 pos) {
        if (pos.Z()>1)
            return true;
        return false;
    };

    print(fisout);
}
