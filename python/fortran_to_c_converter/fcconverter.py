class fcconverter:
    """
    [x] __init__(self, file_name, tabno, print_to_screen=False, print_to_file=False)
    [x] replace_line(self,line)
    [x] replace_with_arg(self, arg1, left_arg1)
    """
    def __init__(self, file_name, tabno, use_compact_line=False, print_to_screen=False, print_to_file=False):
        """
        """
        self.tab = ""
        self.use_compact_line = use_compact_line
        self.dict_parameters = {}
        self.list_dimensions = []
        for i in [0,tabno]:
            self.tab = self.tab+"    "
        self.module_name = ""
        file = open(file_name,'r')
        lines = file.read().splitlines()
        count_line = 0
        for line in lines:
            count_line = count_line + 1
            line_replaced = self.replace_line(line)

            if print_to_screen:
                if line_replaced.find('\n')<0:
                    print(f"{line:80}", f">({count_line:3})>", f"{line_replaced}")
                else:
                    empt = ""
                    count = 0
                    for line_replaced1 in line_replaced.splitlines():
                        if count==0:    print(f"{line:80}", f">({count_line:3})>", f"{line_replaced1}")
                        else:           print(f"{empt:80}", f"{empt:6}>",          f"{line_replaced1}")
                        count = count + 1

            if print_to_file: print(line_replaced, file=file1)

            if count_line==40: break

    def replace_line(self, line):
        """
        """
        line_replaced = ""
        line_post_comment = ""
        if line[0]=='C': # line is comment
            line_comment = line[1:]
            if len(line_comment)!=0: line_replaced = "//"+line_comment
            else: line_replaced = ""
            return line_replaced

        elif line.find("!")>0: # line contain post comment
            line, line_post_comment= line[:line.find("!")], line[line.find("!")+1:].strip()

        line_pre, line_content = line[:5].strip(), line[5:].strip()
        arg1, left_arg1 = line_content[:line_content.find(' ')].strip(), line_content[line_content.find(' '):].strip()
        line_replaced = self.replace_with_arg("", arg1, left_arg1)

        if len(line_post_comment)>0:
            line_replaced = line_replaced + " // " + line_post_comment

        return line_replaced

    def replace_with_arg(self, head_content, arg1, left_arg1):
        """
        """
        line_content = arg1 + " " + left_arg1
        ispace_left_arg1 = left_arg1.find(' ')
        if ispace_left_arg1<0: ispace_left_arg1 = 0
        arg2, left_arg2 = left_arg1[:ispace_left_arg1].strip(), left_arg1[ispace_left_arg1:].strip()
        arg12 = arg1 + " " + arg2

        arg1_type = ""
        if   arg1.find("REAL")==0: arg1_type = "float"
        elif arg1.find("INTEGER*2")==0: arg1_type = "unsigned int"
        elif arg1.find("INTEGER")==0: arg1_type = "int"
        elif arg12.find("DOUBLE PRECISION")==0:
            arg1_type = "double"
            arg1, left_arg1 = arg2, left_arg2 

        line_replaced = ""

        if arg1.find("MODULE")==0:
            self.module_name = left_arg1
            line_replaced = f"#ifndef {self.module_name}\n#define {self.module_name}"#+"\n{"
            print(f'openning {self.module_name}.h')
            file1 = open(f'{self.module_name}.h', 'w')

        elif line_content.find(f"END MODULE {self.module_name}")==0:
            #line_replaced = "}\n#endif"
            line_replaced = "#endif"

        elif len(arg1_type)>0:
            if arg1[len(arg1)-1]==',':
                if len(head_content)==0: head_content = f"{arg1_type:12}"
                else: head_content = head_content + " " + f"{arg1_type:12}"
                return self.replace_with_arg(head_content, arg2, left_arg2)
            else:
                list_def_parameters = []
                for parameter in left_arg1.split(','):
                    list_def_parameters.append(parameter.strip())
                line_replaced = f"{arg1_type:12} {', '.join(list_def_parameters)};"

        elif arg1.find("PARAMETER")==0:
            line_parameters = line_content[line_content.find("(")+1:line_content.rfind(")")]
            for parameter in line_parameters.split(','):
                parameter_name, parameter_value = parameter[:parameter.find("=")].strip(), parameter[parameter.find("=")+1:].strip()
                #parameter = parameter.replace("="," = ")
                line_replaced += f"{parameter_name} = {parameter_value};"
                self.dict_parameters[parameter_name]=parameter_value

        elif arg1.find("DIMENSION")==0:
            list_def_parameters = []
            if len(arg1)>9 and arg1[9]=="(" and arg2=="::": # this line is "type :: variables
                dimension_argument = arg1[10:-1]
                list_dimension_names = left_arg2.split(',')
                for dimension_name in list_dimension_names:
                    list_def_parameters.append(f"{dimension_name}[{dimension_argument}]")

                if self.use_compact_line:
                    line_replaced = f"{', '.join(list_def_parameters)};"
                else:
                    for def_parameter in list_def_parameters:
                        line_replaced = line_replaced + def_parameter + ';\n'
            else:
                for dimension in left_arg1.split(','):
                    dimension_name = dimension[:left_arg1.find("(")]
                    dimension_argument = dimension[left_arg1.find("(")+1:left_arg1.rfind(")")]
                    list_def_parameters.append(f"{dimension_name}[{dimension_argument}]")
                line_replaced = f"double       {', '.join(list_def_parameters)};"

        else:
            line_replaced = f"//TODO? {line_content}"

        if len(head_content)!=0:
            head_content = head_content + " "

        #line_replaced = self.tab + head_content + line_replaced

        if len(line_replaced.splitlines())==1:
            line_replaced = self.tab + head_content + line_replaced
        else:
            line_replaced2 = ""
            for line in line_replaced.splitlines():
                line_replaced2 = line_replaced2 + self.tab + head_content + line.strip() + '\n'
            line_replaced = line_replaced2

        return line_replaced

if __name__ == "__main__":
    help(fcconverter)
