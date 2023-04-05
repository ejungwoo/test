class fcconverter:
    """
    [x] __init__(self, file_name, tabno, print_to_screen=False, print_to_file=False)
    [x] replace_line(self,line)
    [x] replace_with_arg(self, arg1, right_arg1)
    [x] configure_dimension_argument(dimension_name,dimension_argument)
    """
    def __init__(self, file_name, default_tab_no=1, print_to_screen=False, print_to_file=False, use_compact_line=False, use_eval=True):
        """
        """
        self.module_name = ""
        self.use_compact_line = use_compact_line
        self.use_eval = use_eval

        self.set_parameters = set()
        self.dict_parameters = {}
        self.dict_dimensions = {}
        self.dict_sorted_par = {}

        self.default_tab_no = default_tab_no
        self.tab_no = 0
        self.current_line = 0
        self.count_space = 0

        file = open(file_name,'r')
        lines = file.read().splitlines()
        for line in lines:
            self.current_line = self.current_line + 1
            line_replaced = self.replace_line(line)

            if print_to_screen:
                if line_replaced.find('\n')<0:
                    print(f"{line:80}", f"{self.current_line:5} >", f"{line_replaced}")
                else:
                    empt = ""
                    count = 0
                    for line_replaced1 in line_replaced.splitlines():
                        if count==0:    print(f"{line:80}", f"{self.current_line:5} >", f"{line_replaced1}")
                        else:           print(f"{empt:80}", f"{empt:5} >",              f"{line_replaced1}")
                        count = count + 1

            if print_to_file: print(line_replaced, file=file1)

            #if self.current_line==250:
            #    print('\n* List of parameters')
            #    for key, value in self.dict_parameters.items(): print (f"{key:10} = {value}")
            #    break

    def replace_line(self, line_input):
        """
        """
        line_replaced = ""
        line_post_comment = ""

        if len(line_input)==0:
            return ""
        elif line_input[0]=='C': # line_input is comment
            line_full_comment = line_input[1:].strip()
            if len(line_full_comment)!=0: line_replaced = "/// "+line_full_comment
            else: line_replaced = ""
            return line_replaced

        elif line_input.find("!")>0: # line_input contain post comment
            line_input, line_post_comment= line_input[:line_input.find("!")], line_input[line_input.find("!")+1:].strip()

        line_pre, line_content = line_input[:5].strip(), line_input[5:].strip()
        if line_content.find(' ')>0:
            arg1, right_arg1 = line_content[:line_content.find(' ')], line_content[line_content.find(' '):].strip()
        else:
            arg1, right_arg1 = line_content, ""

        self.count_space = 0
        for i in range(len(arg1)):
            if arg1[i]==0: self.count_space = self.count_space + 1 
            else: break
        arg1 = arg1.strip()

        list_line_replaced = self.replace_with_arg("", arg1, right_arg1)

        if len(line_post_comment)>0:
            line_post_comment = " // " + line_post_comment
            #print(line_post_comment)

        #hold_tab = False
        #line1 = list_line_replaced[0].strip()
        #if line1.find("for ")==0 or line1.find("for(")==0 or line1.find("if ")==0 or line1.find("if(")==0 or line1.find("switch")==0 or line1.find("case ")==0:
            #hold_tab = True
        #tab_line = ""
        #    for i in range(self.default_tab_no+self.tab_no-1):
        #        tab_line = tab_line + "    "
        #else:
        #    for i in range(self.default_tab_no+self.tab_no):
        #        tab_line = tab_line + "    "

        tab_line0 = ""
        tab_line1 = ""
        for i in range(self.default_tab_no+self.tab_no-1): tab_line0 = tab_line0 + "    "
        for i in range(self.default_tab_no+self.tab_no):   tab_line1 = tab_line1 + "    "

        #if len(list_line_replaced)==1:
        #    line_replaced = f"tab_line}{list_line_replaced[0]}{line_post_comment}"

        line1 = list_line_replaced[0]
        if line1[:3]=='/1/': line_replaced = f"{tab_line0}{list_line_replaced[0][3:]}{line_post_comment}"
        else:                line_replaced = f"{tab_line1}{list_line_replaced[0]}{line_post_comment}"
        for line in list_line_replaced[1:]:
            if line[:3]=='/1/': line_replaced = line_replaced + f"\n{tab_line0}{line[3:]}{line_post_comment}"
            else:               line_replaced = line_replaced + f"\n{tab_line1}{line}{line_post_comment}"

        #line_replaced = tab_line + f'{line_post_comment}\n{tab_line}'.join(list_line_replaced)

        return line_replaced

    def replace_with_arg(self, arg_type, arg1, right_arg1):
        """
        """
        line_content = arg1 + " " + right_arg1
        ispace_right_arg1 = right_arg1.find(' ')
        if ispace_right_arg1<0: ispace_right_arg1 = 0
        arg2, right_arg2 = right_arg1[:ispace_right_arg1].strip(), right_arg1[ispace_right_arg1:].strip()
        arg12 = arg1 + " " + arg2

        parameter_type = ""
        if   arg1.find("REAL")==0: parameter_type = "float"
        elif arg1.find("INTEGER*2")==0: parameter_type = "unsigned int"
        elif arg1.find("INTEGER")==0: parameter_type = "int"
        elif arg12.find("DOUBLE PRECISION")==0:
            parameter_type = "double"
            arg1, right_arg1 = arg2, right_arg2 

        list_line_replaced = []
        flag_todo = False

        if arg1.find("IF(")==0 and arg1.find(")THEN")>0:
            self.tab_no = self.tab_no + 1
            if_statement = line_content[line_content.find("IF(")+2:line_content.find(")THEN")+1]
            if_statement = if_statement.replace(".LT.","<")
            if_statement = if_statement.replace(".LE.","<=")
            if_statement = if_statement.replace(".GT.",">")
            if_statement = if_statement.replace(".GE.",">=")
            if_statement = if_statement.replace(".EQ.","==")
            if_statement = if_statement.replace(".NE.","!=")
            if_statement = if_statement.replace(".OR.","||")
            if_statement = if_statement.replace(".AND.","&&")
            if_statement = if_statement.replace(".TRUE.","true")
            if_statement = if_statement.replace(".False.","false")
            list_line_replaced.append(f"/1/if {if_statement} "+"{")

        elif arg1.find("ENDIF")==0:
            self.tab_no = self.tab_no - 1
            list_line_replaced.append("}")

        elif arg1.find("DO")==0:
            self.tab_no = self.tab_no + 1

            list_split_comma = right_arg1.split(',')
            if len(list_split_comma)==2 and list_split_comma[0].find("=")>0:
                do_init = list_split_comma[0]
                do_limit = list_split_comma[1]
                do_var, do_init_val = do_init[:do_init.find("=")], do_init[do_init.find("=")+1:]
                list_line_replaced.append(f"/1/for (auto {do_var}={do_init_val}; {do_var}<{do_limit}; ++{do_var}) "+"{")
            else:
                flag_todo = True

        elif arg1.find("ENDDO")==0:
            self.tab_no = self.tab_no - 1
            list_line_replaced.append("}")

        elif arg1.find("SELECT")==0:
            self.tab_no = self.tab_no + 1
            switch_arg = right_arg1.replace("CASE","")
            list_line_replaced.append(f"/1/switch {switch_arg}"+" {")
            self.case_started = False

        elif arg1.find("CASE(")==0:
            case_arg = arg1[arg1.find('(')+1:arg1.find(')')]
            if self.case_started:
                list_line_replaced.append("break;")
            else:
                self.tab_no = self.tab_no + 1
            list_line_replaced.append(f"/1/case {case_arg}:")
            self.case_started = True

        elif line_content.find("END SELECT")==0:
            self.tab_no = self.tab_no - 2
            list_line_replaced.append("}")

        elif arg1.find("write")==0 or arg1.find("WRITE")==0:
            list_value = arg1[10:].split(',') # write(*,*)
            line_replaced = "std::cout << " + ' << " " << '.join(list_value)
            line_replaced = line_replaced + " << std::endl;"
            list_line_replaced.append(line_replaced)

        elif arg1.find("MODULE")==0:
            self.module_name = right_arg1
            list_line_replaced.append(f"#ifndef {self.module_name}")
            list_line_replaced.append(f"#define {self.module_name}")
            print(f'openning {self.module_name}.h')
            file1 = open(f'{self.module_name}.h', 'w')

        elif line_content.find(f"END MODULE {self.module_name}")==0:
            list_line_replaced.append("#endif")

        elif len(parameter_type)>0:
            if arg1[len(arg1)-1]==',':
                return self.replace_with_arg(f"{parameter_type:13}", arg2, right_arg2)
            else:
                list_def_parameters = []
                for parameter_name in right_arg1.split(','):
                    parameter_name = parameter_name.strip()
                    list_def_parameters.append(parameter_name)
                    self.set_parameters.add(parameter_name)
                if self.use_compact_line:
                    list_line_replaced.append(f"{parameter_type:13} {', '.join(list_def_parameters)};")
                else:
                    for parameter_name in list_def_parameters:
                        line_parameter = f"{parameter_type:13} {parameter_name};"
                        list_line_replaced.append(line_parameter)

        elif arg1.find("PARAMETER")==0:
            line_parameters = line_content[line_content.find("(")+1:line_content.rfind(")")]
            list_init_parameters = []
            for parameter in line_parameters.split(','):
                parameter_name, parameter_value = parameter[:parameter.find("=")].strip(), parameter[parameter.find("=")+1:].strip()
                if parameter_name in self.set_parameters:
                    list_init_parameters.append(f"{parameter_name} = {parameter_value};")
                else:
                    if parameter_value.find('.'): parameter_type = "double"
                    else: parameter_type = "int"
                    list_init_parameters.append(f"{parameter_type:13}{parameter_name} = {parameter_value};")
                    self.set_parameters.add(parameter_name)

                if self.use_eval:
                    self.dict_sorted_par = {}
                    for key in sorted(self.dict_parameters, key=len, reverse=True): self.dict_sorted_par[key] = self.dict_parameters[key]
                    for key, value in self.dict_sorted_par.items(): parameter_value = parameter_value.replace(key,value)

                self.dict_parameters[parameter_name]=parameter_value

            list_line_replaced = list_init_parameters

        elif arg1.find("DIMENSION")==0:
            if len(arg_type)==0: arg_type_ = ""
            else: arg_type_ = f"{arg_type:13}"

            list_def_parameters = []
            if len(arg1)>9 and arg1[9]=="(" and arg2=="::": # this line is "type :: variables
                dimension_argument = arg1[10:-1]
                list_dimension_names = right_arg2.split(',')
                for dimension_name in list_dimension_names:
                    dimension_name = dimension_name.strip()
                    dimension_size,dimension_comment = self.configure_dimension_argument(dimension_name,dimension_argument)
                    if len(dimension_comment)>0: dimension_comment = " //TODO? " + dimension_comment
                    list_line_replaced.append(f"{arg_type_}{dimension_name}[{dimension_size}];{dimension_comment}")

            else:
                pass
                for dimension in right_arg1.split(','):
                    dimension_name = dimension[:right_arg1.find("(")]
                    dimension_argument = dimension[right_arg1.find("(")+1:right_arg1.rfind(")")]
                    dimension_size,dimension_comment = self.configure_dimension_argument(dimension_name,dimension_argument)
                    if len(dimension_comment)>0: dimension_comment = " //TODO? " + dimension_comment
                    list_def_parameters.append(f"{dimension_name}[{dimension_size}]")
                list_line_replaced.append(f"{arg_type_}{', '.join(list_def_parameters)}; {dimension_comment}")

        elif arg1.find("CALL")==0:
            list_line_replaced.append(f"{right_arg1} //TODO? CALL")

        elif arg1.find("DATA")==0: flag_todo = True
        elif arg1.find("IMPLICIT")==0: flag_todo = True
        elif arg1=="END": flag_todo = True

        else:
            line_content = line_content.replace("ATAN(","TMath::Atan(")
            line_content = line_content.replace("SQRT(","TMath::Sqrt(")
            line_content = line_content.replace("ALog(","TMath::Log(")
            line_content = line_content.replace("EXP(","TMath::Exp(")
            line_content = line_content.replace("SINH(","TMath::SinH(")
            list_line_replaced.append(f"{line_content}")

        if flag_todo:
            list_line_replaced.append(f"//TODO? {line_content}")

        return list_line_replaced

    def configure_dimension_argument(self,dimension_name,dimension_argument):
        dimension_comment = ""
        list_arg_range = []
        list_arg_diff = []
        for arg in dimension_argument.split(','):
            if arg.find(':')>0: arg_low, arg_high = "("+arg[:arg.find(':')]+")", "("+arg[arg.find(':')+1:]+")"
            else:               arg_low, arg_high = "0", "("+arg+")"
            list_arg_diff.append(arg_high + "-" + arg_low)
            list_arg_range.append([arg_low,arg_high])

        self.dict_dimensions[dimension_name] = list_arg_range

        if self.use_eval:
            list_arg_diff2 = []
            for arg_diff in list_arg_diff:
                self.dict_sorted_par = {}
                for key in sorted(self.dict_parameters, key=len, reverse=True): self.dict_sorted_par[key] = self.dict_parameters[key]
                for key, value in self.dict_sorted_par.items(): arg_diff = arg_diff.replace(key,value)
                arg_diff = eval(arg_diff)
                ##############################
                arg_diff2 = int(arg_diff)
                if arg_diff2!=arg_diff:
                    dimension_comment = f"Dimension size is {arg_diff}!!! converting it to int"
                arg_diff = arg_diff2
                ##############################
                list_arg_diff2.append(str(arg_diff))
            list_arg_diff = list_arg_diff2

        dimension_size = ','.join(list_arg_diff)

        return dimension_size, dimension_comment

if __name__ == "__main__":
    help(fcconverter)
