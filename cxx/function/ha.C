void ff(double par[6], double val[6])
{
    val[0] = par[0]*2;
    val[1] = par[1]*2;
    val[2] = par[2]*2;
    val[3] = par[3]*2;
    val[4] = par[4]*2;
    val[5] = par[5]*2;
}

void ha()
{
    double parameters[6] = {1,2,3,4,5,6};
    double values[6] = {0};
    ff(parameters, values);
    cout << values[0] << endl;
    cout << values[1] << endl;
    cout << values[2] << endl;
    cout << values[3] << endl;
    cout << values[4] << endl;
    cout << values[5] << endl;
}
