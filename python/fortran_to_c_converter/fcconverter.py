import os

class fcconverter:
    """
    [x] __init__(self, file_name, tabno, print_to_screen=False, print_to_file=False)
    [x] replace_with_arg(self, arg1, right_arg1)
    [x] configure_dimension_argument(dimension_name,dimension_argument)
    [x] find_open_close(line_content,notation_open,closetion_open,ignore_while,before_name)
    [] cofig_fortran_variables
    """
    def __init__(self, file_name, default_tab_no=1, print_to_screen=False, print_to_file=False, use_compact_line=False, use_eval=True, limit_line_no = -1):
        """
        """
        self.oupt_path = "source"
        self.use_compact_line = use_compact_line
        self.use_eval = use_eval
        self.module_name = ""
        self.print_to_file = print_to_file
        self.print_to_screen = print_to_screen

        self.set_parameters = set()
        self.dict_parameters = {}
        self.dict_dimensions = {}

        self.default_tab_no = default_tab_no
        self.tab_no = 0
        self.current_line = 0
        self.count_tab_space = 0

        self.file_out = None
        self.file_main = None

        if self.print_to_file:
            os.mkdir(self.oupt_path,exist_ok=True)
            file_name_out = os.path.join(self.oupt_path,file_name.replace('.for',".C"))
            self.file_main = open(f'{file_name_out}', 'w')
            self.file_out = self.file_main

        i_continue = -1
        file = open(file_name,'r')
        list_line_input = file.read().splitlines()
        for i_line in range(len(list_line_input)):
            self.current_line = self.current_line + 1

            line_input0 = list_line_input[i_line]
            line_input = line_input0

            line_replaced = ""
            line_post_comment = ""
            arg_type = ""

            if i_continue >= i_line:
                line_replaced = "// Added to previous line"

            else:
                i_continue = i_line
                while True:
                    i_continue = i_continue + 1
                    if i_continue < len(list_line_input):
                        line_input1 = list_line_input[i_continue]
                        if len(line_input1)>6 and line_input1[0]==' ' and line_input1[5]!=' ':
                            ##########################################################
                            # add next line
                            ##########################################################
                            line_input1 = line_input1[6:]
                            line_post_comment0 = ""
                            if line_input.find('!')>0: # line_input contain post comment
                                line_input, line_post_comment0 = line_input[:line_input.find("!")], line_input[line_input.find("!"):].strip()
                                if len(line_post_comment0)>0:
                                    line_post_comment0 = "  " + line_post_comment0
                            line_input = line_input.rstrip() + line_input1.strip() + line_post_comment0
                            ##########################################################
                        else:
                            i_continue = i_continue - 1
                            break
                    else:
                        i_continue = i_continue -1
                        break

                char0 = line_input[0] if len(line_input)>0 else ""

                if len(line_input)==0:
                    line_replaced = ""

                elif char0=='c' or char0=='C' or char0=='*' or char0=='d' or char0=='D' or char0=='!': # line_input is comment
                    line_full_comment = line_input[1:].strip()
                    if len(line_full_comment)!=0: line_replaced = "/// "+line_full_comment
                    else: line_replaced = ""

                else:
                    if line_input.find('!')>0: # line_input contain post comment
                        line_input, line_post_comment= line_input[:line_input.find("!")], line_input[line_input.find("!")+1:].strip()

                    ############################################################################
                    line_pre, line_content = line_input[:5].strip(), line_input[5:].strip()
                    if line_content.find(' ')>0: arg1, right_arg1 = line_content[:line_content.find(' ')], line_content[line_content.find(' '):].strip()
                    else:                        arg1, right_arg1 = line_content, ""

                    self.count_tab_space = 0
                    for i in range(len(arg1)):
                        if arg1[i]==0: self.count_tab_space = self.count_tab_space + 1
                        else: break

                    arg1 = arg1.strip()
                    ############################################################################
                    list_line_replaced, add_comment_at_last = self.replace_with_arg(arg_type, arg1, right_arg1)
                    ############################################################################
                    if len(add_comment_at_last)>0:
                        line_post_comment = line_post_comment + add_comment_at_last
                    if len(line_post_comment)>0:
                        line_post_comment = " // " + line_post_comment
                    ############################################################################

                    tab_line0 = ""
                    tab_line1 = ""
                    r0 = self.default_tab_no+self.tab_no-1
                    r1 = self.default_tab_no+self.tab_no
                    if r0 < 0: r0 = 0
                    for i in range(r0): tab_line0 = tab_line0 + "    "
                    for i in range(r1): tab_line1 = tab_line1 + "    "

                    if len(list_line_replaced)>0:
                        line1 = list_line_replaced[0]
                        if line1[:3]=='/1/': line_replaced = f"{tab_line0}{list_line_replaced[0][3:]}{line_post_comment}"
                        else:                line_replaced = f"{tab_line1}{list_line_replaced[0]}{line_post_comment}"

                    for line in list_line_replaced[1:]:
                        if line[:3]=='/1/': line_replaced = line_replaced + f"\n{tab_line0}{line[3:]}{line_post_comment}"
                        else:               line_replaced = line_replaced + f"\n{tab_line1}{line}{line_post_comment}"

            if self.print_to_screen:
                if line_replaced.find('\n')<0:
                    print(f"{line_input0:80}", f"{self.current_line:5} >", f"{line_replaced}")
                else:
                    line_empty = ""
                    count = 0
                    for line_replaced1 in line_replaced.splitlines():
                        if count==0:    print(f"{line_input0:80}", f"{self.current_line:5} >", f"{line_replaced1}")
                        else:           print(f"{line_empty:80}", f"{line_empty:5} >",        f"{line_replaced1}")
                        count = count + 1

            if self.print_to_file: print(line_replaced, file=file_out)

            if limit_line_no>0:
                if self.current_line==limit_line_no:
                    print('\n* List of parameters')
                    for key, value in self.dict_parameters.items(): print (f"{key:10} = {value}")
                    break

    def replace_with_arg(self, arg_type, arg1, right_arg1):
        """
        """
        line_content = arg1 + " " + right_arg1
        ispace_right_arg1 = right_arg1.find(' ')
        if ispace_right_arg1<0: ispace_right_arg1 = 0
        arg2, right_arg2 = right_arg1[:ispace_right_arg1].strip(), right_arg1[ispace_right_arg1:].strip()
        arg12 = arg1 + " " + arg2
        add_comment_at_last = ""

        parameter_type = ""
        if   arg1.find("REAL")==0: parameter_type = "float"
        elif arg1.find("INTEGER*2")==0: parameter_type = "unsigned int"
        elif arg1.find("INTEGER")==0: parameter_type = "int"
        elif arg1.find("CHARACTER*")==0:
            #i_comma = arg1.find(",")
            #if i_comma<0:
            #size_charactor = arg1[arg1.find("*")+1:]
            #size_charactor = arg1[arg1.find("*")+1:arg1.find(",")]
            parameter_type = "TString"
        elif arg12.find("DOUBLE PRECISION")==0:
            parameter_type = "double"
            arg1, right_arg1 = arg2, right_arg2 

        list_line_replaced = []
        flag_todo = False

        line_content = line_content.replace("ATAN(","TMath::Atan(")
        line_content = line_content.replace("SQRT(","TMath::Sqrt(")
        line_content = line_content.replace("ALog(","TMath::Log(")
        line_content = line_content.replace("EXP(","TMath::Exp(")
        line_content = line_content.replace("SINH(","TMath::SinH(")

        dict_sorted_dim = {}
        for key in sorted(self.dict_dimensions, key=len, reverse=True): dict_sorted_dim[key] = self.dict_dimensions[key]
        for key, value in dict_sorted_dim.items():
            while True:
                i_key = line_content.find(key+"(")
                if i_key>=0:
                    before_key, after_key = line_content[:i_key], line_content[i_key:]
                    i_name, i_open, i_close = self.find_open_close(after_key)

                    dim_arg = after_key[i_open+1:i_close]
                    arg_low, arg_high = value[0], value[1]
                    dim_arg_new = dim_arg + f"-{arg_low}"

                    dim_old = after_key[:i_open] + '[' + dim_arg_new + ']'
                    dim_new = after_key[:i_open] + '[' + dim_arg_new + ']'
                    after_key_new = dim_new + after_key[i_close+1:]
                    line_content = before_key + after_key_new

                    if arg_low!='0':
                        add_comment_at_last = add_comment_at_last + f" *{dim_old}->{dim_new}"
                else:
                    break


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
            i_name, i_open, i_close = self.find_open_close(line_content)
            list_value = line_content[i_close+1:].split(',')

            line_replaced = "std::cout << " + ' << " " << '.join(list_value)
            line_replaced = line_replaced.replace("'",'"')
            line_replaced = line_replaced + " << std::endl;"
            line_replaced = line_replaced + " // " + line_content[:i_close+1]
            list_line_replaced.append(line_replaced)

        elif arg1.find("MODULE")==0:
            self.module_name = right_arg1
            file_name_out = os.path.join(self.oupt_path,self.module_name+".h")
            list_line_replaced.append(f"/1/#ifndef {self.module_name} // {file_name_out}")
            list_line_replaced.append(f"/1/#define {self.module_name}")

            if self.print_to_file:
                print(f'openning {file_name_out}')
                self.file_out = open(f'{file_name_out}', 'w')

        elif line_content.find(f"END MODULE {self.module_name}")==0:
            if self.print_to_file:
                print("#endif", file=file_out) # todo
                self.file_out = self.file_main
            if self.print_to_screen:
                list_line_replaced.append("/1/#endif")
            self.module_name = ""

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
                    dict_sorted_par = {}
                    for key in sorted(self.dict_parameters, key=len, reverse=True): dict_sorted_par[key] = self.dict_parameters[key]
                    for key, value in dict_sorted_par.items(): parameter_value = parameter_value.replace(key,value)

                self.dict_parameters[parameter_name]=parameter_value

            list_line_replaced = list_init_parameters


        elif arg1.find("DATA")==0:
            right_arg1
            i_name, i_open, i_close = self.find_open_close(right_arg1,notation_open="/",notation_close="/",ignore_while="'")
            par_name = right_arg1[i_name:i_open]
            par_values = right_arg1[i_open+1:i_close]
            if par_values.find(','):
                count_values = 0
                for value in par_values.split(','):
                    value = cofig_fortran_variables(value)
                    list_line_replaced.append(f"{par_name}[{count_values}] = {value}")
                    count_values = count_values + 1
            else:
                list_line_replaced(f"{par_name}={par_values}")

        elif arg1.find("DIMENSION")==0:
            if len(arg_type)<2: arg_type_ = "double"
            else: arg_type_ = f"{arg_type:13}"

            list_def_parameters = []

            if len(arg1)>9 and arg1[9]=="(" and arg2=="::": # this line is "type :: variables
                dimension_arguments = arg1[10:-1]
                list_dimension_names = right_arg2.split(',')
                for dimension_name in list_dimension_names:
                    dimension_name = dimension_name.strip()
                    dimension_size,dimension_comment = self.configure_dimension_argument(dimension_name,dimension_arguments)
                    if len(dimension_comment)>0: dimension_comment = " //TODO? " + dimension_comment
                    list_line_replaced.append(f"{arg_type_}{dimension_name}[{dimension_size}];{dimension_comment}")

            else:
                right_arg1 = right_arg1.replace('),' ,')^')
                right_arg1 = right_arg1.replace(') ,',')^')
                for dimension_par in right_arg1.split('^'):
                    dimension_name = dimension_par[:dimension_par.find("(")]
                    dimension_arguments = dimension_par[dimension_par.find("(")+1:dimension_par.rfind(")")]
                    dimension_size,dimension_comment = self.configure_dimension_argument(dimension_name,dimension_arguments)
                    if len(dimension_comment)>0: dimension_comment = " //TODO? " + dimension_comment
                    list_def_parameters.append(f"{dimension_name}[{dimension_size}]")

                list_line_replaced.append(f"{arg_type_}{', '.join(list_def_parameters)}; {dimension_comment}")

        elif arg1.find("CALL")==0:
            list_line_replaced.append(f"{right_arg1} //TODO? CALL")

        elif arg1.find("READ")==0: flag_todo = True
        elif arg1.find("OPEN")==0: flag_todo = True
        elif arg1.find("CLOSE")==0: flag_todo = True
        elif arg1.find("IMPLICIT")==0: flag_todo = True
        elif arg1=="END": flag_todo = True

        else:
            list_line_replaced.append(f"{line_content}")

        if flag_todo:
            list_line_replaced.append(f"//TODO? {line_content}")

        return list_line_replaced, add_comment_at_last

    def configure_dimension_argument(self,dimension_name,dimension_arguments):
        dimension_comment = ""
        list_arg_range = []
        list_arg_diff = []
        for arg in dimension_arguments.split(','):
            if arg.find(':')>0: arg_low, arg_high = "("+arg[:arg.find(':')]+")", "("+arg[arg.find(':')+1:]+")"
            else:               arg_low, arg_high = "0", "("+arg+")"
            #list_arg_diff.append(arg_high + "-" + arg_low + "+1")
            list_arg_diff.append(arg_high + "-" + arg_low)
            list_arg_range.append(arg_low)
            list_arg_range.append(arg_high)

        self.dict_dimensions[dimension_name] = list_arg_range

        if self.use_eval:
            list_arg_diff2 = []
            for arg_diff in list_arg_diff:
                dict_sorted_par = {}
                for key in sorted(self.dict_parameters, key=len, reverse=True): dict_sorted_par[key] = self.dict_parameters[key]
                for key, value in dict_sorted_par.items(): arg_diff = arg_diff.replace(key,value)
                arg_diff = eval(arg_diff)
                ##############################
                arg_diff2 = int(arg_diff)
                if arg_diff2!=arg_diff:
                    dimension_comment = f"Dimension size is {arg_diff}!!! converting it to int"
                arg_diff = arg_diff2
                ##############################
                list_arg_diff2.append(str(arg_diff))
            list_arg_diff = list_arg_diff2

        #dimension_size = ','.join(list_arg_diff)
        dimension_size = ']['.join(list_arg_diff)

        return dimension_size, dimension_comment

    def find_open_close(self,line_content,notation_open="(",notation_close=")",ignore_while="'",before_name=[' ','=','(',',','*']):
        found_open = False
        ignore_open = False
        count_inner_open = 0
        i_name = 0
        i_open = -1
        i_close = -1
        count_char = -1

        for char in line_content:

            if found_open==False:
                if char in before_name:
                    i_name = count_char+1

            count_char = count_char + 1
            if char==ignore_while:
                if ignore_open:
                    ignore_open = False
                else:
                    ignore_open = True

            if ignore_open == False:

                if char==notation_open:
                    if found_open:
                        if notation_open!=notation_close:
                            count_inner_open = count_inner_open + 1
                    else:
                        found_open = True
                        i_open = count_char

                if char==notation_close:
                    if count_inner_open==0:
                        if count_char==i_open:
                            pass
                        else:
                            i_close = count_char
                            break
                    else:
                        count_inner_open = count_inner_open - 1

        i_close = count_char
        return i_name, i_open, i_close


    def cofig_fortran_variables(self, variable):
        pass

if __name__ == "__main__":
    help(fcconverter)
