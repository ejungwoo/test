class Logger
{
    public:
        Logger(const std::string& fileName, bool logToFile = true, bool logToConsole = true)
        : fLogFile(logToFile ? fileName : ""), fLogToConsole(logToConsole)
        {
        }

        // for message
        template<typename T> Logger& operator<<(const T& value)
        {
            if (fLogToConsole) { std::cout << value; }
            if (fLogFile.is_open()) { fLogFile << value; }
            return *this;
        }

        // for endl
        Logger &operator<<(std::ostream&(*f)(std::ostream&))
        {
            if (fLogToConsole) { std::cout << *f; }
            if (fLogFile.is_open()) { fLogFile << *f; }
            return *this;
        }

    private:
        std::ofstream fLogFile;
        bool fLogToConsole;
};

void test() {
    // Log to both console and file
    Logger logger("mylog.txt");
    logger << "this is message from logger" << endl;;

    // Log only to file
    //Logger ("mylog.txt", true, false);

    // Log only to console
    //Logger ("mylog.txt", false, true);

    // Don't log at all
    //Logger ("mylog.txt", false, false);
}
