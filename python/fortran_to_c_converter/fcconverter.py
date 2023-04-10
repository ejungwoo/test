import os

class fcconverter:
    """
    [x] __init__(self, file_name, tabno, print_to_screen=False, print_to_file=False)
    [x] replace_with_arg(self, arg1, right_arg1)
    [x] configure_dimension_argument(dimension_name,dimension_argument)
    [x] find_open_close(line_content,notation_open,closetion_open,ignore_while,before_name)
    [x] config_fortran_variables(variable)
    """
    def __init__(self, file_name, default_tab_no=0, print_to_screen=False, print_to_file=False, use_compact_line=False, use_eval=True, limit_line_no = -1, use_module_file = True):
        """
        """
        self.oupt_path = "source"
        self.use_compact_line = use_compact_line
        self.use_eval = use_eval
        self.module_name = ""
        self.print_to_file = print_to_file
        self.print_to_screen = print_to_screen

        self.default_tab_no = default_tab_no
        self.tab_no = 0
        self.tab_after = False
        self.current_line = 0

        self.module_run = False
        self.end_module_after = False
        self.line_is_module = False
        self.use_module_file = use_module_file
        self.switch_to_main_file_after = False

        ################################# list
        self.set_parameters = set()
        self.dict_parameters = {}
        self.dict_dimensions = {}

        ################################# file
        self.file_out = None
        self.file_main = None
        self.file_module = None
        self.file_name_out = ""
        self.file_module_name_out = ""

        if self.print_to_file:
            os.makedirs(self.oupt_path,exist_ok=True)
            self.file_name_out = os.path.join(self.oupt_path,file_name.replace('.for',".C"))
            self.file_main = open(f'{self.file_name_out}', 'w')
            self.file_out = self.file_main
            if self.use_module_file:
                self.file_module_name_out = os.path.join(self.oupt_path,file_name.replace('.for',"_modules.h"))
                self.file_module = open(f'{self.file_module_name_out}', 'w')


        file = open(file_name,'r')
        list_line_input = file.read().splitlines()
        for module_run in [True,False]:
        #for module_run in [False]:
            self.module_run = module_run
            self.current_line = 0
            i_merged = -1
            for i_line in range(len(list_line_input)):
                self.current_line = self.current_line + 1

                line_input0 = list_line_input[i_line]
                line_input = line_input0

                line_replaced = ""
                list_line_post_comment = []

                ################################# merge lines
                if i_merged >= i_line:
                    line_input = "! Added to previous line"
                else:
                    i_merged = i_line
                    while True:
                        i_merged = i_merged + 1
                        if i_merged < len(list_line_input):
                            line_input1 = list_line_input[i_merged]
                            if len(line_input1)>6 and line_input1[0]==' ' and line_input1[5]!=' ':
                                ##########################################################
                                # add next line
                                ##########################################################
                                line_input1 = line_input1[6:]
                                line_post_comment = ""
                                if line_input.find('!')>0: # line_input contain post comment
                                    line_input, line_post_comment = line_input[:line_input.find("!")], line_input[line_input.find("!")+1:].strip()
                                    if len(line_post_comment)>0:
                                        line_post_comment = "/// " + line_post_comment
                                        list_line_post_comment.append(line_post_comment)
                                #line_input = line_input.rstrip() + line_post_comment + line_input1.strip()
                                line_input = line_input.rstrip() + line_input1.strip()
                                #print(line_input,line_post_comment)
                                ##########################################################
                            else:
                                i_merged = i_merged - 1
                                break
                        else:
                            i_merged = i_merged -1
                            break




                if len(line_input)==0:
                    line_replaced = ""

                else:
                    ############################################################################
                    list_line_replaced = self.replace_with_arg(line_input)
                    ############################################################################
                    count_comment = 0
                    for comment in list_line_post_comment:
                        list_line_replaced.insert(count_comment,comment)
                        count_comment = count_comment + 1

                    tab_line0 = ""
                    tab_line1 = ""
                    r0 = self.default_tab_no + self.tab_no-1
                    r1 = self.default_tab_no + self.tab_no
                    if r0 < 0: r0 = 0
                    for i in range(r0): tab_line0 = tab_line0 + "    "
                    for i in range(r1): tab_line1 = tab_line1 + "    "
                    if self.tab_after:
                        self.tab_no = self.tab_no + 1
                        self.tab_after = False

                    if len(list_line_replaced)>0:
                        line1 = list_line_replaced[0]
                        if line1[:2]=='<<': line_replaced = f"{tab_line0}{line1[2:]}"
                        else:               line_replaced = f"{tab_line1}{line1}"

                    for line in list_line_replaced[1:]:
                        if line[:2]=='<<': line_replaced = line_replaced + f"\n{tab_line0}{line[2:]}"
                        else:              line_replaced = line_replaced + f"\n{tab_line1}{line}"


                skip_print = False
                if self.module_run==True  and self.line_is_module==False: skip_print = True
                if self.module_run==False and self.line_is_module==True : skip_print = True
                if self.end_module_after:
                    self.end_module_after = False
                    self.line_is_module = False

                if skip_print==False:
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

                    if self.print_to_file: print(line_replaced, file=self.file_out)

                if self.switch_to_main_file_after:
                    self.file_out = self.file_main
                    self.switch_to_main_file_after = False

                if limit_line_no>0:
                    if self.current_line==limit_line_no:
                        print('\n* List of parameters')
                        for key, value in self.dict_parameters.items(): print (f"{key:10} = {value}")
                        break

    def replace_with_arg(self, line_input):
        """
        """
        list_line_replaced = []

        i_ii = line_input.find('!')
        if i_ii>0: # line_input contain post comment
            line_post_comment = line_input[i_ii+1:].strip()
            line_input = line_input[:i_ii]
            list_line_replaced.append(f"/// {line_post_comment}")

        #########
        line_pre = line_input[:5].strip()
        #########
        line_content = line_input[5:].strip()
        #########
        arg1 = line_content[:line_content.find(' ')].strip() if line_content.find(' ')>0 else line_content
        #########
        right_arg1 = line_content[line_content.find(' '):].strip() if line_content.find(' ')>0 else ""
        #########

        ispace_right_arg1 = right_arg1.find(' ')
        if ispace_right_arg1<0: ispace_right_arg1 = 0

        #########
        arg2 = right_arg1[:ispace_right_arg1].strip()
        #########
        right_arg2 = right_arg1[ispace_right_arg1:].strip()
        #########
        arg12 = arg1 + " " + arg2
        #########
        char0 = line_pre[0] if len(line_pre)>0 else ""
        #########

        ispace_right_arg2 = right_arg2.find(' ')
        if ispace_right_arg2<0: ispace_right_arg2 = 0

        #########
        arg3 = right_arg2[:ispace_right_arg2].strip()
        #########
        right_arg3 = right_arg2[ispace_right_arg2:].strip()
        #########

        self.count_tab_space = 0
        for i in range(len(arg1)):
            if arg1[i]==0:
                self.count_tab_space = self.count_tab_space + 1
            else:
                break

        parameter_type0 = ""
        parameter_type1 = ""
        if arg1.find("LOGICAL")==0:
            parameter_type0 = "LOGICAL"
            parameter_type1 = "bool"
        if arg1.find("REAL")==0:
            parameter_type0 = "REAL"
            parameter_type1 = "float"
        elif arg1.find("INTEGER*2")==0:
            parameter_type0 = "INTEGER*2"
            parameter_type1 = "unsigned int"
        elif arg1.find("INTEGER")==0:
            parameter_type0 = "INTEGER"
            parameter_type1 = "int"
        elif arg1.find("CHARACTER*")==0:
            parameter_type0 = "CHARACTER*"
            parameter_type1 = "TString"
        elif arg12.find("DOUBLE PRECISION")==0:
            parameter_type0 = "DOUBLE PRECISION"
            parameter_type1 = "double"
            arg1, right_arg1 = arg2, right_arg2 

        flag_todo = False
        line_type = ""

        line_content = self.config_fortran_variables(line_content)

        if char0=='c' or char0=='C' or char0=='*' or char0=='d' or char0=='D' or char0=='!': # line_content is comment
            line_type = "Comment"
            line_full_comment = line_input[1:].strip()
            if len(line_full_comment)!=0: line_replaced = "/// "+line_full_comment
            else: line_replaced = ""

        elif arg1.find("IF(")==0 and arg1.find(")THEN")>0:
            line_type = "if"
            #self.tab_no = self.tab_no + 1
            self.tab_after = True
            if_statement = line_content[line_content.find("IF(")+2:line_content.find(")THEN")+1]
            if_statement = self.config_fortran_variables(if_statement)
            #list_line_replaced.append(f"<<if {if_statement} "+"{")
            list_line_replaced.append(f"if {if_statement} "+"{")

        elif arg1.find("ELSEIF(")==0 and arg1.find(")THEN")>0:
            line_type = "else if"
            self.tab_no = self.tab_no - 1
            self.tab_after = True
            if_statement = line_content[line_content.find("ELSEIF(")+6:line_content.find(")THEN")+1]
            if_statement = self.config_fortran_variables(if_statement)
            #list_line_replaced.append( "<<}")
            #list_line_replaced.append(f"<<else if {if_statement} "+"{")
            list_line_replaced.append("}")
            list_line_replaced.append(f"else if {if_statement} "+"{")

        elif arg1.find("ELSE(")==0:
            line_type = "else"
            self.tab_no = self.tab_no - 1
            self.tab_after = True
            #list_line_replaced.append("<<}")
            #list_line_replaced.append("<<else {")
            list_line_replaced.append("}")
            list_line_replaced.append("else {")

        elif arg1.find("ENDIF")==0:
            line_type = "end of if"
            self.tab_no = self.tab_no - 1
            list_line_replaced.append("}")

        elif arg1.find("DO")==0:
            line_type = "for"
            #self.tab_no = self.tab_no + 1
            self.tab_after = True

            list_split_comma = right_arg1.split(',')
            if len(list_split_comma)==2 and list_split_comma[0].find("=")>0:
                do_init = list_split_comma[0]
                do_limit = list_split_comma[1]
                do_var, do_init_val = do_init[:do_init.find("=")], do_init[do_init.find("=")+1:]
                #list_line_replaced.append(f"<<for (auto {do_var}={do_init_val}; {do_var}<{do_limit}; ++{do_var}) "+"{")
                list_line_replaced.append(f"for (auto {do_var}={do_init_val}; {do_var}<{do_limit}; ++{do_var}) "+"{")
            else:
                flag_todo = True

        elif arg1.find("ENDDO")==0:
            line_type = "end of for"
            self.tab_no = self.tab_no - 1
            list_line_replaced.append("}")

        elif arg1.find("SELECT")==0:
            line_type = "case"
            self.tab_after = True
            switch_arg = right_arg1.replace("CASE","")
            #list_line_replaced.append(f"<<switch {switch_arg}"+" {")
            list_line_replaced.append(f"switch {switch_arg}"+" {")
            self.case_started = False

        elif arg1.find("CASE(")==0:
            line_type = "case option"
            case_arg = arg1[arg1.find('(')+1:arg1.find(')')]
            if self.case_started:
                list_line_replaced.append("break;")
            else:
                #self.tab_no = self.tab_no + 1
                self.tab_after = True
            #list_line_replaced.append(f"<<case {case_arg}:")
            list_line_replaced.append(f"case {case_arg}:")
            self.case_started = True

        elif line_content.find("END SELECT")==0:
            line_type = "end of case"
            self.tab_no = self.tab_no - 2
            list_line_replaced.append("}")

        elif arg1.find("write")==0 or arg1.find("WRITE")==0:
            line_type = "write"
            i_name, i_open, i_close = self.find_open_close(line_content)
            list_value = line_content[i_close+1:].split(',')

            line_replaced = "std::cout << " + ' << " " << '.join(list_value)
            line_replaced = line_replaced.replace("'",'"')
            line_replaced = line_replaced + " << std::endl;"
            line_replaced = line_replaced + " // " + line_content[:i_close+1]
            list_line_replaced.append(line_replaced)

        elif arg1.find("MODULE")==0:
            line_type = "module"
            self.line_is_module = True
            self.module_name = right_arg1
            file_name_out = os.path.join(self.oupt_path,self.module_name+".h")
            if self.use_module_file:
                file_name_out = self.file_module_name_out

            if self.print_to_file:
                if self.use_module_file:
                    self.file_out = self.file_module
                else:
                    print(f'openning {file_name_out}')
                    self.file_out = open(f'{file_name_out}', 'w')

            list_line_replaced.append(f"<<#ifndef {self.module_name} // {file_name_out}")
            list_line_replaced.append(f"<<#define {self.module_name}")

        elif line_content.find(f"END MODULE {self.module_name}")==0:
            line_type = "end of module"
            self.end_module_after = True
            if self.print_to_file:
                self.switch_to_main_file_after = True
                #print("#endif", file=file_out) # todo
                #self.file_out = self.file_main
            list_line_replaced.append("<<#endif")
            list_line_replaced.append("")
            self.module_name = ""

        elif line_content.find("DIMENSION")>=0:
            line_type = "array"
            if arg1.find("DIMENSION")==0:
                if len(parameter_type1)<2: parameter_type_ = "double"
                else: parameter_type_ = parameter_type1
            elif line_content.find(parameter_type0)==0:
                parameter_type_ = parameter_type1
                arg1 = arg2
                arg2 = arg3
                right_arg2 = right_arg3

            list_def_parameters = []

            if len(arg1)>9 and arg1[9]=="(" and arg2=="::": # this line is "type :: variables
                dimension_arguments = arg1[10:-1]
                list_dimension_names = right_arg2.split(',')
                for dimension_name in list_dimension_names:
                    dimension_name = dimension_name.strip()
                    dimension_size,dimension_comment = self.configure_dimension_argument(dimension_name,dimension_arguments)
                    if len(dimension_comment)>0: dimension_comment = " //TODO? " + dimension_comment
                    list_line_replaced.append(f"{parameter_type_:13}{dimension_name}[{dimension_size}];{dimension_comment}")

            else:
                right_arg1 = right_arg1.replace('),' ,')^')
                right_arg1 = right_arg1.replace(') ,',')^')
                for dimension_par in right_arg1.split('^'):
                    dimension_name = dimension_par[:dimension_par.find("(")]
                    dimension_arguments = dimension_par[dimension_par.find("(")+1:dimension_par.rfind(")")]
                    dimension_size,dimension_comment = self.configure_dimension_argument(dimension_name,dimension_arguments)
                    if len(dimension_comment)>0: dimension_comment = " //TODO? " + dimension_comment
                    list_def_parameters.append(f"{dimension_name}[{dimension_size}]")

                list_line_replaced.append(f"{parameter_type_:13}{', '.join(list_def_parameters)}; {dimension_comment}")

        elif len(parameter_type1)>0:
            line_type = "parameter definition"
            #if arg1[len(arg1)-1]==',': return self.replace_with_arg(f"{parameter_type1:13}", arg2, right_arg2)
            list_def_parameters = []
            for parameter_name in right_arg1.split(','):
                parameter_name = parameter_name.strip()
                list_def_parameters.append(parameter_name)
                self.set_parameters.add(parameter_name)
            if self.use_compact_line:
                list_line_replaced.append(f"{parameter_type1:13} {', '.join(list_def_parameters)};")
            else:
                for parameter_name in list_def_parameters:
                    line_parameter = f"{parameter_type1:13} {parameter_name};"
                    list_line_replaced.append(line_parameter)

        elif arg1.find("PARAMETER")==0:
            line_type = "parameter const initialize"
            line_parameters = line_content[line_content.find("(")+1:line_content.rfind(")")]
            list_init_parameters = []
            for parameter in line_parameters.split(','):
                parameter_name, parameter_value = parameter[:parameter.find("=")].strip(), parameter[parameter.find("=")+1:].strip()
                if parameter_name in self.set_parameters:
                    list_init_parameters.append(f"{parameter_name} = {parameter_value};")
                else:
                    if parameter_value.find('.'): parameter_type_ = "const double"
                    else: parameter_type_ = "const int"
                    list_init_parameters.append(f"{parameter_type_:13}{parameter_name} = {parameter_value};")
                    self.set_parameters.add(parameter_name)

                if self.use_eval:
                    dict_sorted_par = {}
                    for key in sorted(self.dict_parameters, key=len, reverse=True): dict_sorted_par[key] = self.dict_parameters[key]
                    for key, value in dict_sorted_par.items(): parameter_value = parameter_value.replace(key,value)

                self.dict_parameters[parameter_name]=parameter_value

            list_line_replaced = list_init_parameters


        elif arg1.find("DATA")==0:
            line_type = "parameter initialize"
            right_arg1
            i_name, i_open, i_close = self.find_open_close(right_arg1,notation_open="/",notation_close="/",ignore_while="'")
            par_name = right_arg1[i_name:i_open]
            par_values = right_arg1[i_open+1:i_close]
            if par_values.find(','):
                count_values = 0
                for value in par_values.split(','):
                    value = self.config_fortran_variables(value)
                    list_line_replaced.append(f"{par_name}[{count_values}] = {value}")
                    count_values = count_values + 1
            else:
                list_line_replaced(f"{par_name}={par_values}")

        elif arg1.find("CALL")==0:
            line_type = "function"
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

        return list_line_replaced

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


    def config_fortran_variables(self, content):
        content = content.replace(".TRUE.","true")
        content = content.replace(".False.","false")

        content = content.replace("'",'"')

        content = content.replace("ATAN(","TMath::Atan(")
        content = content.replace("SQRT(","TMath::Sqrt(")
        content = content.replace("ALog(","TMath::Log(")
        content = content.replace("EXP(","TMath::Exp(")
        content = content.replace("SINH(","TMath::SinH(")

        content = content.replace(".LT.","<")
        content = content.replace(".LE.","<=")
        content = content.replace(".GT.",">")
        content = content.replace(".GE.",">=")
        content = content.replace(".EQ.","==")
        content = content.replace(".NE.","!=")
        content = content.replace(".OR.","||")
        content = content.replace(".AND.","&&")

        dict_sorted_dim = {}
        for key in sorted(self.dict_dimensions, key=len, reverse=True):
            dict_sorted_dim[key] = self.dict_dimensions[key]

        for key, value in dict_sorted_dim.items():
            while True:
                i_key = content.find(key+"(")
                if i_key>=0:
                    before_key, after_key = content[:i_key], content[i_key:]
                    i_name, i_open, i_close = self.find_open_close(after_key)

                    dim_arg = after_key[i_open+1:i_close]
                    arg_low, arg_high = value[0], value[1]
                    if arg_low!=0:
                        dim_arg_new = dim_arg + f"-{arg_low}"

                    dim_old = after_key[:i_open] + '[' + dim_arg_new + ']'
                    dim_new = after_key[:i_open] + '[' + dim_arg_new + ']'
                    if arg_low!='0':
                        dim_new = after_key[:i_open] + '[' + dim_arg_new + f'/*{dim_old}->{dim_new}*/]'
                    after_key_new = dim_new + after_key[i_close+1:]
                    content = before_key + after_key_new

                else:
                    break

        return content

if __name__ == "__main__":
    help(fcconverter)
