void test()
{
    int count = 0;
    cout << "enter 'x' for exit" << endl;
    while (1) {
        char keyinput = cin.get();
        cout << count++ << ")  " << keyinput << endl;
        if (keyinput=='x') {
            return;
        }
    }
}
