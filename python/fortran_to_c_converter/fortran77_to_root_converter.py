import os

class fcconverter:
    """
    [x] __init__(self, file_name, default_tab_no=0, print_to_screen=False, print_to_file=False, use_compact_line=False, use_eval=True, limit_line_no = -1, use_module_file = False):
    [x] replace_with_arg(self, arg1, right_arg1)
    [x] configure_dimension_argument(dimension_name,dimension_argument)
    [x] find_open_close(line_content,notation_open,closetion_open,ignore_while,before_name)
    [x] split2(line_content,delim,ignore_while)
    [x] config_fortran_line(variable)
    [x] config_types(func_arg)
    [x] set_and_debug_line_type(line_content,line_type):
    """
    def __init__(self, file_name, default_tab_no=0, print_to_screen=False, print_to_file=False, use_compact_line=False, use_eval=True, limit_line_no = -1, use_module_file = False, par_file=""):
        """
        """
        self.oupt_path = "source"
        self.file_name = file_name
        self.use_compact_line = use_compact_line
        self.use_eval = use_eval
        self.module_name = ""
        self.print_to_file = print_to_file
        self.print_to_screen = print_to_screen

        self.default_tab_no = default_tab_no
        self.tab_no = 0
        self.detab_now = 0
        self.tab_init = False
        self.tab_after = False
        self.tab_just_this_line = False
        self.current_line = 0
        self.tab_sign = ""

        self.module_run = False
        self.start_module_now = False
        self.end_module_after = False
        self.line_is_module = False
        self.use_module_file = use_module_file
        self.switch_to_main_file_after = False
        self.func_return_par = ""

        ################################# list
        self.set_parameters = set()
        self.dict_par_value = {}
        self.dict_par_type = {}
        self.dict_dimensions = {}
        self.dict_par_replace = {}

        ################################# file
        self.file_out = None
        self.file_main = None
        self.file_module = None
        self.file_name_out = ""
        self.file_name_out_module = ""

        if len(par_file)!=0:
            file_par_replace = open(par_file)
            list_par_replace = file_par_replace.read().splitlines()
            dict_par_replace = {}
            for line in list_par_replace:
                i_comment = line.find("#") if line.find("#")>0 else len(line)
                line = line[:i_comment].strip()
                if line == "":
                    continue
                name_old = line.split()[0]
                name_new = line.split()[1]
                dict_par_replace[name_old] = name_new
            for key in sorted(dict_par_replace, key=len, reverse=True):
                self.dict_par_replace[key] = dict_par_replace[key]

        self.file_name0 = self.file_name
        if self.file_name0.find("/")>0:
            self.file_name0 = self.file_name[self.file_name0.find("/")+1:]

        if self.print_to_file:
            os.makedirs(self.oupt_path,exist_ok=True)
            self.file_name_out = os.path.join(self.oupt_path,self.file_name0.replace('.for',".C"))
            self.file_main = open(f'{self.file_name_out}', 'w')
            self.file_out = self.file_main
            if self.use_module_file:
                self.file_name_out_module = os.path.join(self.oupt_path,self.file_name0.replace('.for',"_modules.h"))
                self.file_module = open(f'{self.file_name_out_module}', 'w')


        file = open(file_name,'r')
        list_line_input = file.read().splitlines()
        for module_run in [True,False]:
            self.set_parameters = set()
            self.module_run = module_run
            self.current_line = 0
            self.tab_no = 0
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
                    self.tab_sign = ""
                    line_replaced = ""

                else:
                    ############################################################################
                    list_line_replaced = self.replace_with_arg(line_input)
                    ############################################################################

                    count_comment = 0
                    for comment in list_line_post_comment:
                        list_line_replaced.insert(count_comment,comment)
                        count_comment = count_comment + 1

                    if self.tab_init:
                        self.tab_no = 0
                        self.tab_sign = f"[{self.tab_no}(i)]"
                        self.tab_init = False
                    elif self.detab_now != 0:
                        self.tab_no = self.tab_no + self.detab_now
                        if self.detab_now > 0:
                            self.tab_sign = f"[{self.tab_no}(+{self.detab_now})]"
                        else:
                            self.tab_sign = f"[{self.tab_no}({self.detab_now})]"
                        self.detab_now = 0
                    else:
                        self.tab_sign = f"[{self.tab_no}]"


                    if self.tab_just_this_line:
                        self.tab_no = self.tab_no + 1
                        self.tab_sign = f"[{self.tab_no}(+-)]"

                    tab_line0 = ""
                    tab_line1 = ""
                    r0 = self.default_tab_no + self.tab_no-1
                    r1 = self.default_tab_no + self.tab_no
                    if r0 < 0: r0 = 0
                    for i in range(r0): tab_line0 = tab_line0 + "    "
                    for i in range(r1): tab_line1 = tab_line1 + "    "

                    if self.tab_just_this_line:
                        self.tab_no = self.tab_no - 1

                    if self.tab_after:
                        #self.tab_no = self.tab_no + 1
                        self.tab_after = False
                        self.detab_now = 1

                    if len(list_line_replaced)>0:
                        line1 = list_line_replaced[0]
                        if line1[:2]=='<<': line_replaced = f"{tab_line0}{line1[2:]}"
                        else:               line_replaced = f"{tab_line1}{line1}"

                    for line in list_line_replaced[1:]:
                        if line[:2]=='<<': line_replaced = line_replaced + f"\n{tab_line0}{line[2:]}"
                        else:              line_replaced = line_replaced + f"\n{tab_line1}{line}"

                    for name_old, name_new in self.dict_par_replace.items():
                        line_replaced = line_replaced.replace(name_old,name_new)

                if self.start_module_now:
                    self.line_is_module = True
                    self.start_module_now = False
                    if self.module_run==True:
                        self.file_out = open(f'{self.file_name_out_module}', 'w')

                skip_print = False
                if self.module_run==True and self.line_is_module==False: skip_print = True
                if self.module_run==False and self.line_is_module==True: skip_print = True

                if self.end_module_after:
                    self.end_module_after = False
                    self.line_is_module = False
                    self.switch_to_main_file_after = True

                if skip_print==False:
                    if self.print_to_screen:
                        if line_replaced.find('\n')<0:
                            joint = f"{self.current_line} {self.tab_sign}"
                            print(f"{line_input0:80}", f"{joint:12} >", f"{line_replaced}")
                        else:
                            line_empty = ""
                            count = 0
                            for line_replaced1 in line_replaced.splitlines():
                                if count==0: joint = f"{self.current_line} {self.tab_sign}"
                                else:        joint = line_empty
                                print(f"{line_empty:80}", f"{joint:12} >", f"{line_replaced1}")
                                count = count + 1

                    if self.print_to_file:
                        print(line_replaced, file=self.file_out)

                if self.switch_to_main_file_after:
                    self.file_out = self.file_main
                    self.switch_to_main_file_after = False

                if limit_line_no>0:
                    if self.current_line==limit_line_no:
                        print('\n* List of parameters')
                        for key, value in self.dict_par_value.items(): print (f"{key:10} = {value}")
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
        line_header = line_input[:6].strip()
        #########
        line_content = line_input[6:].strip()
        #########
        arg1 = line_content[:line_content.find(' ')].strip() if line_content.find(' ')>0 else line_content
        #########
        right_arg1 = line_content[line_content.find(' '):].strip() if line_content.find(' ')>0 else ""
        #########

        ispace_right_arg1 = right_arg1.find(' ')
        if ispace_right_arg1<0: ispace_right_arg1 = len(right_arg1)

        #########
        arg2 = right_arg1[:ispace_right_arg1].strip()
        #########
        right_arg2 = right_arg1[ispace_right_arg1:].strip()
        #########
        arg12 = arg1 + " " + arg2
        #########
        char0 = line_header[0] if len(line_header)>0 else ""
        #########
        label = line_header[1:5].strip()
        if char0!=" ":
            label = ""
        #########

        ispace_right_arg2 = right_arg2.find(' ')
        if ispace_right_arg2<0: ispace_right_arg2 = len(right_arg2)

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

        line_content = self.config_fortran_line(line_content)

        if len(label)>0:
            list_line_replaced.append(f"///TOOD {label} come to here")


        if line_header=="AFT_IF":
            self.tab_just_this_line

        if char0=='c' or char0=='C' or char0=='*' or char0=='d' or char0=='D' or char0=='!': # line_content is comment
            self.set_and_debug_line_type(line_content,"Comment")
            line_full_comment = line_input[1:].strip()
            if len(line_full_comment)!=0: list_line_replaced.append(f"///({char0}) "+line_full_comment)
            #else: list_line_replaced.append("/// "+line_full_comment)
            else: list_line_replaced.append("")

        elif arg1.find("IF(")==0:
            self.set_and_debug_line_type(line_content,"if")
            i_name, i_open, i_close = self.find_open_close(line_content)
            if_statement = line_content[i_open:i_close+1]
            if_statement = self.config_fortran_line(if_statement)
            if arg1.find("THEN")>0:
                self.tab_after = True
                list_line_replaced.append(f"if {if_statement} "+"{")
            else:
                list_line_replaced.append(f"if {if_statement}")
                line_input2 = "AFT_IF" + line_content[i_close+1:]
                list_line_replaced.extend(self.replace_with_arg(line_input2))

        elif arg1.find("ELSEIF(")==0 and arg1.find(")THEN")>0:
            self.set_and_debug_line_type(line_content,"else if")
            self.detab_now = -1
            self.tab_after = True
            if_statement = line_content[line_content.find("ELSEIF(")+6:line_content.find(")THEN")+1]
            if_statement = self.config_fortran_line(if_statement)
            list_line_replaced.append("}")
            list_line_replaced.append(f"else if {if_statement} "+"{")

        elif arg1.find("ELSE(")==0:
            self.set_and_debug_line_type(line_content,"else")
            self.detab_now = -1
            self.tab_after = True
            list_line_replaced.append("}")
            list_line_replaced.append("else {")

        elif arg1.find("ENDIF")==0:
            self.set_and_debug_line_type(line_content,"end of if")
            self.detab_now = -1
            list_line_replaced.append("}")

        elif arg1.find("DO")==0:
            self.set_and_debug_line_type(line_content,"for")
            self.tab_after = True

            #list_split_comma = right_arg1.split(',')
            list_split_comma = self.split2(right_arg1)
            if len(list_split_comma)==2 and list_split_comma[0].find("=")>0:
                do_init = list_split_comma[0]
                do_limit = list_split_comma[1]
                do_var, do_init_val = do_init[:do_init.find("=")], do_init[do_init.find("=")+1:]
                list_line_replaced.append(f"for (auto {do_var}={do_init_val}; {do_var}<{do_limit}; ++{do_var}) "+"{")
            else:
                flag_todo = True

        elif arg1.find("ENDDO")==0:
            self.set_and_debug_line_type(line_content,"end of for")
            self.detab_now = -1
            list_line_replaced.append("}")

        elif arg1.find("SELECT")==0:
            self.set_and_debug_line_type(line_content,"case")
            self.tab_after = True
            switch_arg = right_arg1.replace("CASE","")
            list_line_replaced.append(f"switch {switch_arg}"+" {")
            self.case_started = False

        elif arg1.find("CASE(")==0:
            self.set_and_debug_line_type(line_content,"case option")
            case_arg = arg1[arg1.find('(')+1:arg1.find(')')]
            if self.case_started:
                list_line_replaced.append("break;")
            else:
                self.tab_after = True
            list_line_replaced.append(f"case {case_arg}:")
            self.case_started = True

        elif line_content.find("END SELECT")==0:
            self.set_and_debug_line_type(line_content,"end of case")
            self.detab_now = -2
            list_line_replaced.append("}")

        elif arg1.find("write")==0 or arg1.find("WRITE")==0:
            self.set_and_debug_line_type(line_content,"write")
            i_name, i_open, i_close = self.find_open_close(line_content)
            #list_value = line_content[i_close+1:].split(',')
            list_value = self.split2(line_content[i_close+1:])

            line_replaced = "std::cout << " + ' << " " << '.join(list_value)
            #line_replaced = "std::cout << " + ' << '.join(list_value)
            line_replaced = line_replaced.replace("'",'"')
            line_replaced = line_replaced + " << std::endl;"
            line_replaced = line_replaced + " // " + line_content[:i_close+1]
            list_line_replaced.append(line_replaced)

        elif arg1.find("USE")==0:
            self.set_and_debug_line_type(line_content,"use")
            list_line_replaced.append(f'<<#include "{arg2}.h"')

        elif arg1.find("MODULE")==0:
            self.set_and_debug_line_type(line_content,"module")
            self.start_module_now = True
            self.module_name = right_arg1
            if self.use_module_file==False:
                self.file_name_out_module = os.path.join(self.oupt_path,f"{self.module_name}.h")

            list_line_replaced.append(f"<<#ifndef {self.module_name} // {self.file_name}")
            list_line_replaced.append(f"<<#define {self.module_name} // {self.file_name_out_module}")

        elif line_content.find(f"END MODULE {self.module_name}")==0:
            self.set_and_debug_line_type(line_content,"end of module")
            self.end_module_after = True
            list_line_replaced.append("<<#endif")
            list_line_replaced.append("")
            self.module_name = ""

        elif arg1.find("SUBROUTINE")==0:
            self.set_and_debug_line_type(line_content,"subrotine: void function")
            if arg2.find("("):
                i_name, i_open, i_close = self.find_open_close(arg2)
                func_name = right_arg1[i_name:i_open]
                func_arg = right_arg1[i_open+1:i_close]
            else:
                func_name = arg2
                func_arg = ""

            self.tab_after = True
            func_arg = self.config_types(func_arg,True)
            list_line_replaced.append(f"void {func_name}({func_arg}) "+"{")

        elif arg1.find("FUNCTION")==0:
            self.set_and_debug_line_type(line_content,"function: function with return")
            if arg2.find("("):
                i_name, i_open, i_close = self.find_open_close(arg2)
                self.func_return_par = right_arg1[i_name:i_open]
                func_name = f"get_{self.func_return_par}"
                func_arg = right_arg1[i_open+1:i_close]

            self.tab_after = True
            #func_arg = self.config_fortran_line(func_arg)
            #parameter_type_ = self.dict_par_type[self.func_return_par]
            parameter_type_ = "double"
            list_line_replaced.append(f"{parameter_type_} {func_name}({func_arg}) "+"{")

        elif arg1.find("END")==0:
            self.set_and_debug_line_type(line_content,"end of subrotine")
            #self.detab_now = -1
            self.tab_init = -1
            if self.func_return_par:
                list_line_replaced.append(f"return {self.func_return_par};")
                self.func_return_par = ""
            list_line_replaced.append("}")

        elif line_content.find("DIMENSION")>=0:
            self.set_and_debug_line_type(line_content,"array")
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
                #list_dimension_names = right_arg2.split(',')
                list_dimension_names = self.split2(right_arg2)
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
            self.set_and_debug_line_type(line_content,"parameter definition")
            list_def_parameters = []
            list_parameter_names = self.split2(right_arg1)
            for parameter_name in list_parameter_names:
                parameter_name = parameter_name.strip()
                list_def_parameters.append(parameter_name)
                self.set_parameters.add(parameter_name)
                self.dict_par_type[parameter_name]=parameter_type1
            if self.use_compact_line:
                list_line_replaced.append(f"{parameter_type1:13} {', '.join(list_def_parameters)};")
            else:
                for parameter_name in list_def_parameters:
                    line_parameter = f"{parameter_type1:13} {parameter_name};"
                    list_line_replaced.append(line_parameter)

        elif arg1.find("PARAMETER")==0:
            self.set_and_debug_line_type(line_content,"parameter const initialize")
            line_parameters = line_content[line_content.find("(")+1:line_content.rfind(")")]
            list_init_parameters = []
            list_parameter_names = self.split2(line_parameters)
            for parameter in list_parameter_names:
                parameter_name, parameter_value = parameter[:parameter.find("=")].strip(), parameter[parameter.find("=")+1:].strip()
                if parameter_name in self.set_parameters:
                    #print(">>>>>",parameter_name,self.set_parameters)
                    list_init_parameters.append(f"{parameter_name} = {parameter_value};")
                else:
                    if parameter_value.find('E')>0 or parameter_value.find('D')>0 or parameter_value.find('.')>0:
                        parameter_type_ = "const double"
                    else:
                        parameter_type_ = "const int"
                    list_init_parameters.append(f"{parameter_type_:13}{parameter_name} = {parameter_value};")
                    self.set_parameters.add(parameter_name)
                    self.dict_par_type[parameter_name]=parameter_type_

                if self.use_eval:
                    dict_sorted_par = {}
                    for key in sorted(self.dict_par_value, key=len, reverse=True): dict_sorted_par[key] = self.dict_par_value[key]
                    for key, value in dict_sorted_par.items(): parameter_value = parameter_value.replace(key,value)

                self.dict_par_value[parameter_name]=parameter_value

            list_line_replaced = list_init_parameters


        elif arg1.find("DATA")==0:
            self.set_and_debug_line_type(line_content,"parameter initialize")
            right_arg1
            i_name, i_open, i_close = self.find_open_close(right_arg1,notation_open="/",notation_close="/",ignore_while="'")
            par_name = right_arg1[i_name:i_open]
            par_values = right_arg1[i_open+1:i_close]
            if par_values.find(',')>=0:
                count_values = 0
                list_values = self.split2(par_values)
                for value in list_values:
                    value = self.config_fortran_line(value)
                    list_line_replaced.append(f"{par_name}[{count_values}] = {value}")
                    count_values = count_values + 1
            else:
                list_line_replaced.append(f"{par_name}={par_values}")

        elif arg1.find("OPEN")==0:
            self.set_and_debug_line_type(line_content,"open file")
            i_name, i_open, i_close = self.find_open_close(arg1)
            open_args = arg1[i_open+1:i_close]
            list_open_arg = self.split2(open_args)
            if list_open_arg[0].find("=")>0:
                open_file_id = list_open_arg[0].split("=")[1]
            else:
                open_file_id = list_open_arg[0]
            for open_arg in list_open_arg:
                open_and_write = False
                if open_arg.find("FILE")>=0:
                    open_file_name = open_arg.split("=")[1]
                if open_arg.find("WRITE")>0:
                    open_and_write = True
            if open_and_write:
                list_line_replaced.append(f"ofstream file_{open_file_id}({open_file_name});")
            else:
                list_line_replaced.append(f"ifstream file_{open_file_id}({open_file_name});")

        elif arg1.find("CALL")==0:
            self.set_and_debug_line_type(line_content,"function")
            list_line_replaced.append(f"{right_arg1}; //TODO? CALL")

        elif arg1.find("RETURN")==0: flag_todo = True
        elif arg1.find("GOTO")==0: flag_todo = True
        elif arg1.find("READ")==0: flag_todo = True
        elif arg1.find("CLOSE")==0: flag_todo = True
        elif arg1.find("IMPLICIT")==0: flag_todo = True
        #elif arg1=="END": flag_todo = True

        else:
            list_line_replaced.append(f"{line_content};")

        if flag_todo:
            list_line_replaced.append(f"//TODO? {line_content}")

        return list_line_replaced

    def configure_dimension_argument(self,dimension_name,dimension_arguments):
        dimension_comment = ""
        list_arg_range = []
        list_arg_diff = []
        list_arg = self.split2(dimension_arguments)
        for arg in list_arg:
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
                for key in sorted(self.dict_par_value, key=len, reverse=True): dict_sorted_par[key] = self.dict_par_value[key]
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

        if i_name==i_open: i_name = 0
        i_close = count_char
        return i_name, i_open, i_close

    def split2(self, line_content, delim=",", ignore_while='"'):
        ignore_open = False
        count_inner_open = 0
        count_char = -1

        list_of_blocks = []
        block = ""

        for char in line_content:

            count_char = count_char + 1
            if char==ignore_while:
                if ignore_open:
                    ignore_open = False
                else:
                    ignore_open = True

            if ignore_open == False and char==delim:
                list_of_blocks.append(block)
                block = ''
            else:
                block = block + char

        if len(block)>0:
            list_of_blocks.append(block)

        return list_of_blocks


    def config_fortran_line(self, content):
        content = content.replace(".TRUE.","true")
        content = content.replace(".False.","false")

        content = content.replace("'",'"')

        content = content.replace("ABS(","TMath::Abs(")
        content = content.replace("ATAN(","TMath::ATan(")
        content = content.replace("SQRT(","TMath::Sqrt(")
        content = content.replace("ALog(","TMath::Log(")
        content = content.replace("EXP(","TMath::Exp(")
        content = content.replace("SINH(","TMath::SinH(")

        content = content.replace("NINT(","int(")

        content = content.replace(".LT.","<")
        content = content.replace(".LE.","<=")
        content = content.replace(".GT.",">")
        content = content.replace(".GE.",">=")
        content = content.replace(".EQ.","==")
        content = content.replace(".NE.","!=")
        content = content.replace(".OR.","||")
        content = content.replace(".AND.","&&")

        content = content.replace("1D0","1.")
        content = content.replace("2D0","2.")
        content = content.replace("3D0","3.")
        content = content.replace("4D0","4.")
        content = content.replace("0D0","0.")
        content = content.replace("0E)","0.")


        #content = content + ';'

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
                    dim_arg_new = dim_arg
                    if arg_low!='0':
                        if arg_low.find("-")>=0:
                            arg_low = arg_low[:-1].replace("(-","")
                            dim_arg_new = dim_arg + f"+{arg_low}"
                        else:
                            dim_arg_new = dim_arg + f"-{arg_low}"

                    dim_old = after_key[:i_open] + '[' + dim_arg + ']'
                    dim_new = after_key[:i_open] + '[' + dim_arg_new + ']'
                    if arg_low!='0':
                        #dim_new = after_key[:i_open] + '[' + dim_arg_new + f'/*{dim_old}->{dim_new}*/]'
                        dim_new = after_key[:i_open] + '[' + dim_arg_new + ']'
                    after_key_new = dim_new + after_key[i_close+1:]
                    content = before_key + after_key_new

                else:
                    break

        return content

    def config_types(self, func_arg, add_AND=False):
        list_arg = self.split2(func_arg)
        func_arg = ""

        dict_sorted_par = {}
        for key in sorted(self.dict_par_type, key=len, reverse=True):
            dict_sorted_par[key] = self.dict_par_type[key]

        for arg_name in list_arg:
            arg_type = "double"
            for par_name, par_type in dict_sorted_par.items():
                if arg_name == par_name:
                    arg_type = par_type
            if add_AND: func_arg = func_arg + f",{arg_type} &{arg_name}"
            else:       func_arg = func_arg + f",{arg_type} {arg_name}"
        func_arg = func_arg[1:]

        return func_arg

    def set_and_debug_line_type(self,line_content,line_type):
        #print("[set_and_debug_line_type]", f"({line_type})", line_content)
        pass


if __name__ == "__main__":
    help(fcconverter)
