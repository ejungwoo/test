class Logger {
public:
    Logger(const std::string& filename, bool logToFile = true, bool logToConsole = true)
        : logfile_(logToFile ? filename : "")
        , logToConsole_(logToConsole) {
    }

    template<typename T>
    Logger& operator<<(const T& value) {
        if (logToConsole_) {
            std::cout << value;
        }
        if (logfile_.is_open()) {
            logfile_ << value;
        }
        return *this;
    }

private:
    std::ofstream logfile_;
    bool logToConsole_;
};

void test() {
  // Log to both console and file
  Logger logger("data/mylog.txt");
  logger << "asdflaksdfj";

  // Log only to file
  //Logger ("mylog.txt", true, false);

  // Log only to console
  //Logger ("mylog.txt", false, true);

  // Don't log at all
  //Logger ("mylog.txt", false, false);
}
