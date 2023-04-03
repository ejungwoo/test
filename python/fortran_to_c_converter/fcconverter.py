class fcconverter:
    """
    """
    def __init__(self,file_name):
        self.file = open(file_name,'r')
        lines = self.file.read().splitlines()
        for line in lines:
            line_replaced = ""
            if line[0]=='C':
                line_replaced = line[1:]
                if len(line_replaced)!=0:
                    line_replaced = "//"+line_replaced
            else:
                line_5, line_content = line[:5].strip(), line[5:].strip()
                arg1 = line_content[:line_content.find(' ')]
                if arg1.find("REAL")>=0:
                    arg1
                line_replaced = f"{line:5}{line_content}"
            print(f"{line:80}", ">>>>", f"{line_replaced}")

if __name__ == "__main__":
    help(fcconverter)
