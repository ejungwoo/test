import os

class lilakcc:
    """
    Write c++ class with source and header
    - methods:

        [x] add(self,input_lines)
            [x] set_class(self,line0, acc_spec, method_source)
                [x] set_file_name(self,name)
                [x] set_file_path(self,file_path)
                [x] set_class_comment(self, comment)
                [x] add_inherit_class(self, inherit_acc_class)
                [x] set_tab_size(self, tab_size)
            [x] add_method(self,line, acc_spec, method_source)
                [x] make_method(self, line, is_header=True, is_source=False)
            [x] add_par(self,line, lname, gname, acc_spec, par_setter, par_getter, par_init, par_clear, par_print, par_source)
                [x] make_par(self, par_type, par_name, par_init, par_comments)
            [x] add_input_data_array(self, data_class, data_array_gname, data_array_bname, data_array_lname="", single_data_name="data", input_comment="")
            [x] add_output_data_array(self, data_class, data_array_gname, data_array_bname, data_array_lname="", single_data_name="data", input_comment="", data_array_init_size=0, data_persistency=True):

        [x] break_line(self,lines)
        [x] check_method_or_par(self,line):
        [x] make_doxygen_comment(self, comment, add_to="", always_mult_line=False, not_for_doxygen=False, is_persistence=True)
        [x] include_headers(self,includes):

        [x] print_container(self,to_screen=False,to_file=True,print_example_comments=True,
        [x] print_task(self,to_screen=False,to_file=True,print_example_comments=True):
            [x] init_print(self):
    """

    def __init__(self):
        # class
        self.name = ""
        self.path = "./"
        self.comment = ""
        self.tab_size = 4
        self.inherit_list = []

        # for task
        self.data_init_list = []
        self.data_exec_list = []
        self.data_array_def_list = []

        # container 
        self.par_clear_list = []
        self.par_print_list = []
        self.par_copy_list = []

        # general
        self.par_def_list = [[],[],[]]
        self.par_init_list = []
        self.set_full_list = [[],[],[]]
        self.get_full_list = [[],[],[]]
        self.method_header_list = [[],[],[]]
        self.method_source_list = [[],[],[]]

        # include headers
        self.include_root_list = []
        self.include_lilak_list = []
        self.include_other_list = []

        # parameter file
        self.parfile_lines = []
  
    def set_tab_size(self, tab_size):
        """Set tab size"""
        self.tab_size = tab_size
        print("+{:20}: {}".format("Set tab size",tab_size))

    def set_file_name(self,name):
        """Set name of the class"""
        self.name = name
        print("+{:20}: {}".format("Set class",name))
  
    def set_file_path(self,file_path):
        """Set path where files are created"""
        self.path = file_path
        print("+{:20}: {}".format("Set file path",file_path))

    def set_class_comment(self, comment):
        """Description of the class"""
        self.comment = comment 
        print("+{:20}: {}".format("Set class comment",comment))

    def add_inherit_class(self, inherit_acc_class):
        """Description of the class"""
        self.inherit_list.append(inherit_acc_class)
        print("+{:20}: {}".format("Add inherit class",inherit_acc_class))

###########################################################################################################################################
    def add(self, input_lines):
        """ # Make funciton from line
        Add class, parameter or methods by line
        You may use main keywords to notify the start of the group:
            +path      -- set path to file
            +class     -- add class
            +idata     -- add input data container
            +odata     -- add output data container
            +include   -- add headers to be included
            +private   -- add parameter or method as private
            +protected -- add parameter or method as protected
            +public    -- add parameter or method as public

        When defining parameter or method identifying parameter/method will be done automatically.
        Multiline definitions are also allowed.
        ex:
            +include TNothing.h

            +class TEveryting
            +inherit public TSomething
            +inherit public TAnything

            +idata auto fMyData = new TClonesArray("TMyData",100)

            +private double fValue1 = 0.01;
            +private double fValue2 = 0.02;
            +private double fValue3 = 0.03;
            +private double fValue4 = 0.04;

            +public
            double DoSomething(double value1, double value2) {
                fValue += value1;
                fValue -= value2;
                return fValue;
            }

        Sub-keywords exist to support parameter and method definitions.

        ### class sub-keywords:
            +inherit -- inheritance of class ex: public TNamed

        ### input/output data container sub-keywords for 
            +gname  -- set global data container array name
            +lname  -- set local  data container array name
            +bname  -- set parameter name to be registered or registered as branch name
            +pname  -- set local single data container name
            +size   -- set initial size of the data container array
            +persis -- set persistency of branch (True or False). Default is True

        ex:
            +odata auto fMyDataArray = TClonesArray("TMyData",100)
            +lname myDataArray
            +bname firstData
            +pname myData

        ### parameter sub-keywords:
            +gname  -- set global parameter name
            +lname  -- set local  parameter name
            +pname  -- set parameter name to be used in the parameter container
            +persis -- set persistency of parameter (True or False). Default is True
            +setter -- set setter
            +getter -- set getter
            +source -- set content to be included in the Constructor of LKTask
            +init   -- set content to be included in the Init() method of LKTask
            +clear  -- set content to be included in the Clear() method of LKTask
            +print  -- set content to be included in the Print() method of LKTask
            +copy   -- set content to be included in the Copy() method of LKTask
        ex):
            +private TParameter<double> fParameter1 = 0.08;
            +source fParameter1 = new TParameter<double>({pname},-9.99)
            +pname parameter1
            +init fParameter1 -> SetVal({parc} -> GetParString({pname}))
            +clear fParameter1 -> SetVal(-9.99)

        ### method sub-keyword:
            source -- set method to be written in the source
        """

        if len(input_lines)==0:
            print(f"[add()] WARNING1! no input is given!")
            return

        if input_lines.find("\n")<0:
            file_add = open(input_lines, 'r')
            input_lines = file_add.read()

        group = []
        group_list = []
        list_line = input_lines.splitlines()
        list_complete = ["path", "class", "idata", "odata", "include", "private", "protected", "public"]
        list_components = ["comment", "inherit", "gname", "lname", "pname", "bname", "persis", "setter", "getter", "init", "clear", "source", "print", "copy"]

        is_method = True
        head_is_found = False
        for line in list_line:
            if len(line)==0:
                if len(group)>0:
                    group_list.append(group.copy())
                    head_is_found = False
                    group.clear()
            elif line[:2] == '//' or line[:2] == '/*' or line[:2] == ' *' or line[0] == '*' or line.find('+comment')==0:
                group.append(["comment",line])
            elif line[0] == '+':
                ispace = line.find(' ')
                if ispace < 0: ispace = len(line)
                ltype = line[1:ispace] # line type
                content = line[ispace+1:].strip() # line content
                if ltype=='':
                    ltype=='public'
                if ltype in list_complete:
                    if head_is_found == True:
                        if len(group)>0:
                            group_list.append(group.copy())
                            head_is_found = False
                            group.clear()
                    head_is_found = True
                    group.append([ltype,content])
                elif ltype in list_components:
                    group.append([ltype,content])
            else:
                group.append(["",line])
        if len(group)>0:
            group_list.append(group.copy())
            head_is_found = False
            group.clear()

        for group in group_list:

            group_new = []
            i1 = 0
            for i0 in range(len(group)):
                ltype0, line0 = group[i0]
                if (ltype0)==0:
                    continue
                for i1 in range(len(group)):
                    ltype1, line1 = group[i1]
                    if len(ltype1)==0 or ltype1==ltype0:
                        line0 = line0 + "\n" + line1
                    else:
                        break
                group_new.append([ltype0,line0])

            #print("=====================================================")
            #for ltype, line in group_new: print(f"{ltype:15}{ltype0:15}",line)

            print(group_new)

            for ltype0, line0 in group_new:
                if ltype0 in list_complete:
                    break

            if ltype0=='path':
                self.set_file_path(line0)

            elif ltype0=='class':
                class_comment = ""
                list_inherit = []
                for ltype, line in group_new:
                    if ltype=='comment': class_comment = line
                    if ltype=='inherit': list_inherit.append(line)
                self.set_class(line0,class_comment=class_comment, list_inherit=list_inherit)

            elif ltype0=='idata':
                idata_gname = ""
                idata_lname = ""
                idata_pname = ""
                idata_bname = ""
                for ltype, line in group_new:
                    method_source = ""
                    if ltype=='gname': idata_gname = line
                    if ltype=='lname': idata_lname = line
                    if ltype=='pname': idata_pname = line
                    if ltype=='bname': idata_bname = line
                    if ltype=='comment': idata_comment = line
                da_name, d0_class, da_size = self.break_data_array(line0)
                add_input_data_array(self, data_class=d0_class, data_array_gname=idata_gname,
                        data_array_bname=idata_bname, data_array_lname=idata_lname,
                        single_data_name=idata_pname, input_comment=idata_comment)

            elif ltype0=='odata':
                odata_gname = ""
                odata_lname = ""
                odata_pname = ""
                odata_bname = ""
                odata_persis = True
                for ltype, line in group_new:
                    if ltype=='gname':  odata_gname = line
                    if ltype=='lname':  odata_lname = line
                    if ltype=='pname':  odata_pname = line
                    if ltype=='bname':  odata_bname = line
                    if ltype=='comment': odata_comment = line
                    if ltype=='persis': odata_persis = (True if (line.strip().lower())=="true" else False)
                da_name, d0_class, da_size = self.break_data_array(line0)
                add_output_data_array(self, data_class=d0_class, data_array_gname=idata_gname, data_array_bname=idata_bname, data_array_lname=idata_lname,
                        single_data_name=idata_pname, data_array_init_size=d0_size, input_comment=idata_comment, data_persistency=odata_persis)

            elif ltype0=='include':
                self.include_headers(line)

            elif is_method:
                acc_spec = ltype0
                method_source = ""
                for ltype, line in group_new:
                    if ltype=='source': method_source = line
                self.add_method(line0, acc_spec=acc_spec, method_source = method_source)

            else:
                acc_spec = ltype0
                par_gname  = ""
                par_lname  = ""
                par_pname  = ""
                par_persis = True
                par_setter = ""
                par_getter = ""
                par_init   = ""
                par_clear  = ""
                par_print  = ""
                par_copy  = ""
                par_source = ""
                par_comment = ""
                for ltype, line in group_new:
                    if ltype=='gname':  par_gname  = line
                    if ltype=='lname':  par_lname  = line
                    if ltype=='pname':  par_pname  = line
                    if ltype=='persis': par_persis = (True if (line.strip().lower())=="true" else False)
                    if ltype=='setter': par_setter = line
                    if ltype=='getter': par_getter = line
                    if ltype=='init':   par_init   = line
                    if ltype=='clear':  par_clear  = line
                    if ltype=='print':  par_print  = line
                    if ltype=='copy':   par_copy  = line
                    if ltype=='source': par_source = line
                    if ltype=='comment': par_comment = line
                self.add_par(line0, acc_spec=acc_spec, input_comment=par_comment,
                        gname=par_gname, lname=par_lname,
                        pname=par_pname, par_persis=par_persis, 
                        par_setter=par_setter, par_getter=par_getter,
                        par_init=par_init, par_clear=par_clear,
                        par_print=par_print, par_copy=par_copy, par_source=par_source)

###########################################################################################################################################
    def set_class(self, line, class_comment="", list_inherit=[]):
        if line.find('class')==0:
            line = line[line.find('class')+5:].strip()

        if line.find("::")>0:
            line = line[line.find('::')+2:].strip()

        if line.find(":")>0:
            after_colon = line[line.find(':')+1:]
            line = line[:line.find(':')]
            if after_colon.find("{")>=0:
                after_colon = after_colon[:after_colon.find('{')]
            list_classes = after_colon.split(",")
            for class_name in list_classes:
                list_inherit.append(class_name)

        if line.find('class')==0:
            class_name = line[5:].strip()
        else:
            class_name = line.strip()

        self.set_file_name(class_name)
        self.set_class_comment(class_comment)

        for inherit_group in list_inherit:
            self.add_inherit_class(inherit_group)
    
###########################################################################################################################################
    def add_method(self, line, comment="", acc_spec="public", method_source=""):
        if len(method_source)==0: method_source = line
        method_header = self.make_method(line,         comment=comment,is_header=True)
        method_source = self.make_method(method_source,comment=comment,is_source=True)

        ias = {"public" : 0, "protected": 1, "private" : 2}.get(acc_spec, -1)
        self.method_header_list[ias].append(method_header)
        self.method_source_list[ias].append(method_source)

###########################################################################################################################################
    def make_method(self, line, comment="", tab_no=0, is_header=True, is_source=False, in_line=False, omit_semicolon=False):
        is_method, method_type, method_name, method_arguments, method_const, method_init, method_contents, method_comments, comment_type = self.break_line(line)

        tab1 = ' '*(self.tab_size*1)

        if omit_semicolon:
            semicolon = ""
        else:
            semicolon = ";"

        line_const = f" const" if len(method_const)>0 else " "
        line_arguments = "(" + method_arguments + ")"
        #if method_arguments=="X":
        #    line_arguments = ""
        if len(method_arguments)==0:
            line_arguments = "()"

        if len(method_init)>0:
            line_content = " = " + method_init + semicolon
        elif len(method_contents)>0:
            if len(method_const)>0:
                line_const = line_const + " "
            if method_contents.find("\n")>=0 or is_source:
                line_content = "{\n"
                for method_content in method_contents.splitlines():
                    line_content = line_content + tab1 + method_content + "\n"
                line_content = line_content + "}"
            else:
                line_content = " { " + method_contents + " }"
        else:
            line_const = ""
            line_content = semicolon
        if len(method_type)!=0:
            method_type = method_type + " "
        line = f"{method_type}{method_name}{line_arguments}{line_const}{line_content}"
        line = (" "*self.tab_size)*tab_no + line
        line = self.make_doxygen_comment(method_comments,line)
        return line

###########################################################################################################################################
    def add_par(self, lines, 
                acc_spec="public",
                gname="", lname="", pname="", par_persis=True,
                par_setter="", par_getter="",
                par_init="", par_clear="", par_print="", par_copy="",
                par_source="", input_comment=""):
        """ add parameter
        lines               -- Input contents
        acc_spec = "public" -- Access specifier: one of "public", protected", "private"
        gname = ""          -- Global(Field) name used through class. Default : f[lname]
        lname = ""          -- Local name to be used inside the block. 
        pname = ""          -- Parameter name to be used in the parameter container
        par_persis = True   -- Persistency of the parameter (do or do not write in the root file)
        par_setter = ""     -- Contents to be add as Getter.
        par_getter = ""     -- Contents to be add as Setter.
        par_init = ""       -- Contents to be add in the Init() method.
        par_clear = ""      -- Contents to be add in the Clear() method.
        par_print = ""      -- Contents to be add in the Print() method.
        par_copy = ""       -- Contents to be add in the Copy() method.
        par_source = ""     -- Contents to be add in the class constructor.
        """

        is_method, par_type, par_name, par_arguments, par_const, par_initv, par_contents, par_comments, comment_type = self.break_line(lines)
        ias = {"public":0, "protected":1, "private":2}.get(acc_spec, -1)

        ############ general par name ############
        if par_name[0]=="f" and par_name[1].isupper:
            par_name = par_name[1:]

        ############ field parameter name ############
        if len(gname)==0:
            gname = "f" + par_name[0].title()+par_name[1:]

        ############ local parameter name ############
        if len(lname)==0:
            lname = par_name
        if lname==gname:
            print(f"WARNING2! gname({gname}) and lname({lname}) are same! replacing lname to {lname}_.")
            lname = lname + "_"

        ############ parameter name in parameter container ############
        if len(pname)==0:
            pname = par_name

        pname_comment = ""
        if pname.find('#'):
            pname_comment = pname[pname.find('#')+1:]

        if isinstance(par_initv, str)==False: par_initv = str(par_initv)

        use_par_init = False
        if len(par_init)==0:
            par_file_val = par_initv
        else:
            use_par_init = True
            pname2 = par_init[:par_init.find(' ')]
            par_init = par_init.replace("{pname}",pname)
            if pname2!=pname:
                print(f"WARNING3! given pname({pname}) and pname2({pname2}) from par_init, are not same! replacing pname2 to {pname}.")
                pname2 = {pname}
                par_init = pname + ' ' + par_init[par_init.find(' '):]

        ############ parameter task init ############

        line_par_init_in_init = gname
        line_par_comment_in_init = ""
        if   par_type=="bool":        par_type_getpar = "Bool"
        elif par_type=="int":         par_type_getpar = "Int"
        elif par_type=="double":      par_type_getpar = "Double"
        elif par_type=="float":       par_type_getpar = "Double"
        elif par_type=="Bool_t":      par_type_getpar = "Bool"
        elif par_type=="Int_t":       par_type_getpar = "Int"
        elif par_type=="Double_t":    par_type_getpar = "Double"
        elif par_type=="Float":       par_type_getpar = "Double"
        elif par_type=="TString":     par_type_getpar = "String"
        elif par_type=="const char*": par_type_getpar = "String"
        elif par_type=="Color_t":     par_type_getpar = "Color"
        elif par_type=="Width_t":     par_type_getpar = "Width"
        elif par_type=="Size_t":      par_type_getpar = "Size"
        elif par_type=="TVector3":
            par_type_getpar = "V3"
            par_file_val = par_file_val[par_file_val.find('(')+1:par_file_val.find(')')]
            par_file_val = par_file_val.replace(',','  ')
        else:
            line_par_comment_in_init = f"//TODO The type {par_type} is not featured with LKParameterContainer. Please modify Below:" 
            par_type_getpar = par_type
        line_par_init_in_init = f'{gname} = par -> GetPar{par_type_getpar}("{pname}");'

        ############ parameter definition ############
        init_from_header = True
        if use_par_init:
            init_from_header = False
        elif len(par_initv)==0:
            init_from_header = False
        elif par_initv.find('->')>0:
            init_from_header = False
        elif par_initv.find('.')>0:
            if par_initv[par_initv.find('.')+1].isdigit()==False:
                init_from_header = False

        if init_from_header: line_par_definition = f'{par_type} {gname} = {par_initv};'
        else:                line_par_definition = f'{par_type} {gname};'
        line_par_definition = self.make_doxygen_comment(par_comments,line_par_definition,is_persistence=par_persis)

        if use_par_init:     line_par_in_par_container = f'{par_init}'
        else:                line_par_in_par_container = f'{pname} {par_file_val}'
        line_par_definition = self.make_doxygen_comment(pname_comment,line_par_in_par_container,comment_type="#")

        ############ parameter clear ############
        if len(par_clear)==0:
            if use_par_init:
                line_par_in_clear = f'{par_initv};';
            elif len(par_initv)>0:
                line_par_in_clear = f'{gname} = {par_initv};';
            else:
                line_par_in_clear = f'{gname};';
        else:
            line_par_in_clear = make_method(par_clear.replace("{gname}",gname), in_line=True)

        ############ parameter print ############
        if len(par_print)==0:
            if par_type in ["bool", "int", "double", "float", "Bool_t", "Int_t", "Double_t", "Float_t", "TString", "const char*"]:
                line_par_in_print = f'lx_info << "{par_name} : " << {gname} << std::endl;'
            else:
                line_par_in_print = f'//lx_info << "{par_name} : " << {gname} << std::endl;'
        else:
            line_par_in_print = self.make_method(par_print.replace("{gname}",gname), in_line=True)

        ############ settter definition ############
        if len(par_setter)==0:
            set_type = par_type
            set_name = "Set" + par_name[0].title()+par_name[1:]
            line_set_par = self.make_method(f"void {set_name} {set_type} {lname} {gname} = {lname};", in_line=True)
        else:
            line_set_par = self.make_method(par_setter.replace("{gname}",gname), in_line=True)
            is_method, set_type, set_name, dp, dp, dp, dp, dp, dp = self.break_line(line_set_par)
  
        ############ gettter definition ############
        if len(par_getter)==0:
            get_type = par_type
            get_name = "Get" + par_name[0].title()+par_name[1:]
            line_get_par = self.make_method(f"{get_type} {get_name}() const " +"{"+ f"return {gname};"+"}", in_line=True)
        else:
            line_get_par = self.make_method(par_getter.replace("{gname}",gname), in_line=True)
  
        ############ parameter copy ############
        if len(par_copy)==0:
            line_par_in_copy = f"objCopy.{set_name}({gname})"
        else:
            line_par_in_copy = self.make_method(par_copy.replace("{gname}",gname), in_line=True)

        ############  ############  ############
        if len(line_par_comment_in_init)!=0:
            self.par_init_list.append(line_par_comment_in_init);
        self.par_init_list.append(line_par_init_in_init);
        self.par_clear_list.append(line_par_in_clear);
        self.par_print_list.append(line_par_in_print);
        self.par_copy_list.append(line_par_in_copy);
        self.par_def_list[ias].append(line_par_definition);
        self.set_full_list[0].append(line_set_par);
        self.get_full_list[0].append(line_get_par);
        self.parfile_lines.append(line_par_in_par_container)


###########################################################################################################################################
    def make_par(self, line):

        is_method, par_type, par_name, par_arguments, par_const, par_init, par_contents, par_comments, comment_type = self.break_line(lines)
        par_header = self.make_par(par_type=par_type, par_name=par_name, par_init=par_init, par_comments=par_comments)
        ias = {"public":0, "protected":1, "private":2}.get(acc_spec, -1)
        print("==", ias, par_header)

        line_init = f" = {par_init}" if len(par_init)>0 else ""
        line = f"{par_type} {par_name}{line_init};"
        line = self.make_doxygen_comment(par_comments,line)
        return line
        
###########################################################################################################################################
    def make_fline(self, func_full, comment="", tab_no=-1, is_source=False, is_header=False, in_line=False, omit_semicolon=False):
        """Make funciton from line"""
        is_method, func_type, func_name, func_arguments, func_const, func_init, func_contents, func_comments2, comment_type = self.break_line(func_full)

        if   len(comment)==0 and len(func_comments2)!=0: comment = func_comments2
        elif len(comment)!=0 and len(func_comments2)==0: pass
        elif len(comment)!=0 and len(func_comments2)!=0: comment = comment + '\n' + func_comments2

        if   tab_no<-1 and tab_no2>=0: tab_no = tab_no2
        elif tab_no>=0: tab_no = tab_no
        else: tab_no = 0

        if is_source and func_name.find("::")<0: func_full = self.name + "::" + func_name + "(" + func_arguments + ")"
        else:                                    func_full = func_name + "(" + func_arguments + ")"

        if len(func_type)>0: func_full = ' '*(self.tab_size*tab_no) + func_type + " " + func_full
        else:                func_full = ' '*(self.tab_size*tab_no) + func_full

        if (func_const):
            func_full = func_full + " const"

        lines = func_contents.split('\n')

        just_define = False
        mult_line = False
        if in_line==True: pass
        elif is_header:             just_define = True
        elif is_source:             mult_line = True
        elif len(func_contents)==0: just_define = True
        else:                       mult_line = True

        if just_define:
            if omit_semicolon==False:
                func_full = func_full + ";"
        elif mult_line:
            if func_contents=="":
                func_full = func_full + '\n' + ' '*(self.tab_size*tab_no) + "{"
                func_full = func_full + '\n' + ' '*(self.tab_size*tab_no) + "}"
            else:
                for i in range(len(lines)):
                    lines[i] = ' '*(self.tab_size*(tab_no+1)) + lines[i]
                func_full = func_full + '\n' + ' '*(self.tab_size*tab_no) + "{"
                func_full = func_full + '\n' + '\n'.join(lines)
                func_full = func_full + '\n' + ' '*(self.tab_size*tab_no) + "}"
        else:
            if func_contents.isspace():  func_full =  func_full + " {}"
            else:                       func_full =  func_full + " { " + func_contents + " }"
        return self.make_doxygen_comment(comment, func_full)

###########################################################################################################################################
    def check_method_or_par(self,line):
        ic1 = line.find("//")
        #if ic1==0: return False
        line_before_cb = line[:ic1].strip() if line.find("{")>0 else line
        ib1 = line_before_cb.find("(")
        ieq = line_before_cb.find("=")
        if ib1<0 or (ieq>0 and ieq<ib1): return False
        else: return True

###########################################################################################################################################
    def break_data_array(self,lines):
        pre_and_name, tclonesarray_def = lines[:lines.find("=")].strip(), lines[lines.find("=")+1:].strip()

        ispace = pre_and_name.find(" ")
        if space<0: da_name = pre_and_name
        else:       da_name = pre_and_name[space:].strip()

        tclonesarray_def = tclonesarray_def[tclonesarray_def.find("(")+1:tclonesarray_def.rfind(")")]
        arguments = tclonesarray_def.split(',')

        d0_class = arguments[0]
        d0_class = d0_class[d0_class.find('"')+1:d0_class.rfind('"')]
        da_size = int(arguments[1])

        return da_name, d0_class, da_size

###########################################################################################################################################
    def break_line(self,lines):
        """
        Break input line into
        * method:    type, name, argument, const, (init/content), comments
        * parameter: type, name, init
        return True(method)/False(parameter), type, name, arguments, "const"/"", init, contents, comments, comment_type
        """
        ################################################### precomment
        comment_list = []
        line_inprocess = lines
        ic1 = line_inprocess.find("//")
        ibe = line_inprocess.rfind("}")
        # comment_type
        # 0:
        # 1: //
        # 2: ///
        # 3: ///<
        # 4: ///<!
        # 5: //!
        comment_type = ""
        while ic1>=0 and ic1>ibe:
            if ic1==line_inprocess.find("///<!"):
                func_linec = line_inprocess[ic1+5:]
                false_persistency = True
                comment_type = "///<!"
            elif ic1==line_inprocess.find("//!"):
                func_linec = line_inprocess[ic1+3:]
                false_persistency = True
                comment_type = "//!"
            elif ic1==line_inprocess.find("///<"):
                func_linec = line_inprocess[ic1+4:]
                comment_type = "///<"
            elif ic1==line_inprocess.find("///"):
                func_linec = line_inprocess[ic1+3:]
                comment_type = "///"
            else:
                func_linec = line_inprocess[ic1+2:]
                comment_type = "//"
            line_inprocess = line_inprocess[:ic1]
            comment_list.append(func_linec)
            ic1 = line_inprocess.find("//")

        ###################################################
        icb1 = line_inprocess.find("{")
        line_before_cb = line_inprocess
        line_after_cb  = ""
        if icb1>0:
            line_before_cb = line_inprocess[:icb1].strip()
            line_after_cb  = line_inprocess[icb1:].strip()

        ################################################### before_cb
        ib1 = line_before_cb.find("(")
        ieq = line_before_cb.find("=")

        func_type = ""
        func_name = ""
        func_init = ""
        func_arguments = ""
        func_const = ""

        def_parameter = False
        is_method = False
        if ib1<0 or (ieq>0 and ieq>ib1):
            ################################################### def_parameter
            def_parameter = True
            if ieq>0: #par without init
                func_type_name, func_init = line_inprocess[:ieq].strip(), line_inprocess[ieq+1:].strip()
            else: #par with init
                func_type_name = line_inprocess.strip()
                func_init = ""

            icomma = func_type_name.find(",")
            ispace = func_type_name.rfind(" ")
            if ispace<0:
                ispace=0
                #print("------- ERROR1 configuring type and name: ", lines, " -------")
            if icomma>0:
                while func_type_name[icomma-1]==' ':
                    icomma = icomma-1
                ispace = func_type_name[:icomma].rfind(" ")
            func_type, func_names = func_type_name[:ispace].strip(), func_type_name[ispace:].strip()

            if func_names.find(",")>0:
                for par in func_names.split(","):
                    func_name = func_name + ", " + par.strip()
                func_name = func_name[2:]
            else:
                func_name = func_names

        else:
            ################################################### is_method
            is_method = True
            line_before_rb, line_after_rb = line_before_cb[:ib1].strip(), line_before_cb[ib1:].strip()

            func_arguments = line_after_rb
            ib2 = func_arguments.rfind(")")
            if ib2<ieq:
                func_arguments, func_init = line_after_rb[:ieq].strip(), line_after_rb[ieq:].strip()

            if ib2>0:
                func_arguments, func_x_par = func_arguments[1:ib2].strip(), func_arguments[ib2:].strip()
                #print(func_arguments, " ################ ", func_x_par)
                if func_x_par.find("const")>=0:
                    func_const = "const"
            elif ib2==0:
                func_arguments = ""
            elif ib2<0:
                print("ERROR2 configuring parmeters no ')': ", lines)
                return False

            ispace = line_before_rb.rfind(" ")
            if ispace<0:
                func_type, func_name = "", line_before_rb
            else:
                func_type, func_name = line_before_rb[:ispace].strip(), line_before_rb[ispace:].strip()

        ################################################### configure
        if len(func_name)>0:
            if func_name[len(func_name)-1]==';':
                func_name = func_name[:len(func_name)-1].strip()

        if len(func_init)>0:
            if func_init[len(func_init)-1]==';':
                func_init = func_init[:len(func_init)-1].strip()

        if func_name[0]=='*':
            func_name = func_name[1:]
            func_type = func_type + "*"

        ################################################### after_cb
        if is_method:
            ib3 = line_after_cb.find("{")
            ib4 = line_after_cb.find("}")
            if ib3>=0:
                if ib3+1==ib4:
                    func_contents = ";"
                else:
                    func_contents = line_after_cb[ib3+1:ib4].strip()
                    if len(func_contents)==0: func_contents = ""
                    else:
                        if func_contents[0]=="\n": func_contents = func_contents[1:]
                        if func_contents[len(func_contents)-1]=="\n": func_contents = func_contents[:len(func_contents)-1]
            else:
                func_contents = ""
        else:
            func_contents = ""

        func_comments = '\n'.join(comment_list)

        return (True if is_method else False), func_type, func_name, func_arguments, func_const, func_init, func_contents, func_comments, comment_type

    def make_doxygen_comment(self, comment, add_to="", always_mult_line=False, not_for_doxygen=False, is_persistence=True, comment_type=""):
        """Make doxygen comment

        add_to (string) -- If add_to parameter is set True, comment will be put after (before)
                           Return comment, is_mult_line where is_mult_line is True when comment is multi-line if add_to is set False. 
        always_mult_line (bool) -- The comments are assumed that it is multi-line and use /** [...] */
        not_for_doxygen (bool) -- If True: /** -> /*, ///< -> //
        """
        if comment_type.strip()=="#":
            always_mult_line = False

        multi_line_comment = False
        single_line_comment = False
        if always_mult_line or "\n" in comment or "\r\n" in comment:
            multi_line_comment = True
        else:
            single_line_comment = True

        if is_persistence and len(comment)==0:
            return add_to
        else:
            if always_mult_line or "\n" in comment or "\r\n" in comment:
                lines = comment.split('\n')
                for i in range(len(lines)):
                    lines[i] = ' * ' + lines[i]
                else:
                    if not_for_doxygen: lines.insert(0,"/*")
                    else:                 lines.insert(0,"/**")
                    lines.append(" */")
                comment = '\n'.join(lines)
                return comment + add_to
            else:
                if len(comment_type)!=0:
                    if   not_for_doxygen: comment_type = "//"
                    elif is_persistence:  comment_type = "///<"
                    else:                 comment_type = "///<!"
                comment = " " + comment_type + " " + comment;
                return add_to + comment

    def include_headers(self,includes):
        """Include header files assuming that includes are separated by spaces or line-break"""
        if len(includes)==0:
            return
        header_list = includes.replace(' ','\n')
        header_list = includes.split('\n')
        for header in header_list:
            if header[:8]!="#include":
                if header[0]=='"' or header[0]=='<':
                    header_full = "#include "+header
                else:
                    header_full = "#include \""+header+"\""
            else:
                header_full = header

            if header[0]=="T":      self.include_root_list.append(header_full)
            elif header[:2]=="LK":  self.include_lilak_list.append(header_full)
            else:                   self.include_other_list.append(header_full)

    def add_input_data_array(self, data_class, data_array_gname, data_array_bname, data_array_lname="", single_data_name="data", input_comment=""):
        ############ field name ############
        if data_array_gname[0]=="f" and data_array_gname[1].isupper:
            par_name = par_name[1:]
        else:
            data_array_name_field = "f" + data_array_gname[0].title()+data_array_gname[1:]

        ############ local name ############
        if len(data_array_lname)==0:
            data_array_lname = data_array_gname
            if data_array_lname==data_array_name_field:
                data_array_lname = data_array_lname + "_"

        self.data_init_list.append(f'fTrackArray = run -> GetBranchA("{data_array_bname}");')

        num_data = "num" + data_array_bname[0].title()+data_array_bname[1:]
        i_data = "i" + data_array_bname[0].title()+data_array_bname[1:]
        tab1 = ' '*(self.tab_size*1)
        self.data_exec_list.append(f"""
//Call {single_data_name} from {data_array_name_field} and get data value
int {num_data} = {data_array_name_field} -> GetEntriesFast();
for (int {i_data} = 0; {i_data} < {num_data}; ++{i_data})""" + "\n{" + f"""
{tab1}auto *{single_data_name} = ({data_class} *) {data_array_name_field} -> At({i_data});
{tab1}//auto value = {single_data_name} -> GetDataValue(); ...
"""+"}")


    def add_output_data_array(self, data_class, data_array_gname, data_array_bname, data_array_lname="", single_data_name="data",
                              data_array_init_size=0, input_comment="", data_persistency=True):
        ############ field name ############
        if data_array_gname[0]=="f" and data_array_gname[1].isupper:
            par_name = par_name[1:]
        else:
            data_array_name_field = "f" + data_array_gname[0].title()+data_array_gname[1:]

        ############ persistency ############
        data_array_name_persis = data_array_name_field + "Persistency"
        data_array_name_persis_lc = data_array_lname + "Persistency"
        self.add_private_par("bool", data_array_name_persis_lc, "true" if data_persistency else "false")

        ############ branch name ############
        #if len(data_array_bname)==0: data_array_bname = data_array_gname;

        ############ local name ############
        if len(data_array_lname)==0:
            data_array_lname = data_array_gname
            if data_array_lname==data_array_name_field:
                data_array_lname = data_array_lname + "_"

        self.data_array_def_list.append(f"TClonesArray *{data_array_name_field} = nullptr;")

        if data_array_init_size>0: self.data_init_list.append(f'{data_array_name_field} = new TClonesArray("{data_class}");')
        else:                      self.data_init_list.append(f'{data_array_name_field} = new TClonesArray("{data_class}",{data_array_init_size});')
        self.data_init_list.append(f'run -> RegisterBranch("{data_array_bname}", {data_array_name_field}, {data_array_name_persis});')

        num_data = "num" + data_array_bname[0].title()+data_array_bname[1:]
        i_data = "i" + data_array_bname[0].title()+data_array_bname[1:]
        tab1 = ' '*(self.tab_size*1)
        self.data_exec_list.append(f"""
//Construct (new) {single_data_name} from {data_array_name_field} and set data value
int {num_data} = {data_array_name_field} -> GetEntriesFast();
for (int {i_data} = 0; {i_data} < {num_data}; ++{i_data})""" + "\n{" + f"""
{tab1}auto *{single_data_name} = ({data_class} *) {data_array_name_field} -> ConstructedAt({i_data});
{tab1}//{single_data_name} -> SetData(value); ...
"""+"}")

    def init_print(self):
        if os.path.exists(self.path)==False:
            os.mkdir(self.path)

    def print_container(self,to_screen=False, to_file=True, print_example_comments=False,
                        inheritance='public LKContainer', includes='LKContainer.h'):
        """Print header and source file of lilak container class content to screen or file

        to_screen (bool ; False) -- If True, print container to screen
        to_file (bool ; True) -- If True, print container to file ({path}/{name}.cpp, {path}/{name}.h) 
        print_example_comments (bool ; True) -- Print comments that helps you filling up reset of the class.
        inheritance (string ; 'LKContainer') -- Class inheritance.
        includes (string ; 'LKContainer.h') -- headers to be included separated by space
        """
        self.init_print()
        br1 = "{"
        br2 = "}"

        self.include_headers('TClonesArray.h')
        self.include_headers('LKLogger.h')
        self.include_headers(includes)
        self.include_headers('<iostream>')

        inherit_class_list = inheritance.split(',')
        inherit_class = inherit_class_list[0]
        inherit_class = inherit_class.replace('public',' ')
        inherit_class = inherit_class.replace('private',' ')
        inherit_class = inherit_class.replace('private',' ')
        inherit_class = inherit_class.strip()

        tab1 = ' '*(self.tab_size*1)
        tab2 = ' '*(self.tab_size*2)
        etab1 = '\n'+tab1
        etab2 = '\n'+tab2

        name_upper = self.name.upper()
        header_define = f"""#ifndef {name_upper}_HH
#define {name_upper}_HH
"""
        header_container="""Remove this comment block after reading it through
Or use print_example_comments=False option to omit printing

# Example LILAK container class

## Essential
 - Write constructor containing Clear() method.
 - Write Clear() method.

More about Clear() method:
It is recommended that LKTasks create data container array using TClonesArray class.
For the detail of TClonesArray, see https://root.cern/doc/master/classTClonesArray.html
or https://opentutorials.org/module/2860/19477 (for the simple version in Korean)
In LKTask, Clear("C") is called to TClonesArray at the start of the Exec() of LKTask classes.
This means that all containers 

Version number (2nd par. in ClassDef of source file) should be changed if the class has been modified.
This notifiy users that the container has been update in the new LILAK (or side project version).

## Recommended
 - Documentaion like this!
 - Write Print() to see what is inside the container;

## If you have time
 - Write Copy() for copying object
"""
        if print_example_comments:
            header_container = self.make_doxygen_comment(header_container,not_for_doxygen=True)
            header_container = header_container + "\n"
        else:
            header_container = ""
        header_include_lilak = '\n'.join(sorted(set(self.include_lilak_list)))
        header_include_root = '\n'.join(sorted(set(self.include_root_list)))
        header_include_other = '\n'.join(sorted(set(self.include_other_list)))
        header_description = self.make_doxygen_comment(self.comment)
        header_class = f"class {self.name} : {inheritance}" + "\n{"

        source_include = f'#include "{self.name}.h"'

        ############## public ##############
        header_class_public = ' '*self.tab_size + "public:"
        if print_example_comments:
            constructor_content = "// It is essential to place Clear() method inside the constructor for TClonesArray feature.\nClear();"
        else:
            constructor_content = "Clear();"
        header_constructor = self.make_method(self.name, tab_no=2, is_header=True)
        header_destructor = self.make_method("virtual ~"+self.name, tab_no=2, is_header=True)
        header_clear = self.make_method("virtual void Clear(Option_t *option)", tab_no=2, is_header=True)
        header_print = self.make_method("virtual void Print(Option_t *option) const;", tab_no=2, is_header=True)
        header_copy = self.make_method("virtual void Copy (TObject &object) const;",  tab_no=2, is_header=True)

        header_getter = tab2 + etab2.join(self.get_full_list[0])
        header_setter = tab2 + etab2.join(self.set_full_list[0])
        header_public_par = tab2 + etab2.join(self.par_def_list[0])

        self.par_clear_list.insert(0,f"{tab1}{inherit_class}::Clear(option);")
        clear_content = '\n'.join(self.par_clear_list)

        self.par_print_list.insert(0,"//TODO You will probability need to modify here")
        self.par_print_list.insert(1,f"{inherit_class}::Print();")
        self.par_print_list.insert(2,f'lx_info << "{self.name} container" << std::endl;')
        print_content = '\n'.join(self.par_print_list)

        self.par_copy_list.insert(0,"//TODO You should copy data from this container to objCopy")
        self.par_copy_list.insert(1,f"{inherit_class}::Copy(object);")
        self.par_copy_list.insert(2,f"auto objCopy = ({self.name} &) object;")
        copy_content = '\n'.join(self.par_copy_list)

        source_constructor = self.make_method(f"{self.name}::{self.name}() {br1}{constructor_content}{br2}", 0, is_source=True)
        source_clear = self.make_method(f"void Clear(Option_t *option) const {br1}{clear_content}{br2}", 0, is_source=True)
        source_print = self.make_method(f"void Print(Option_t *option) const {br1}{print_content}{br2}", 0, is_source=True)
        source_copy = self.make_method (f"void Copy (TObject  &object) const {br1}{copy_content}{br2}", 0, is_source=True)

        ############## protected ##############
        header_class_protected = ' '*self.tab_size + "protected:"
        header_protected_par = tab2 + etab2.join(self.par_def_list[1])

        ############## private ##############
        header_class_private = ' '*self.tab_size + "private:"
        header_private_par = tab2 + etab2.join(self.par_def_list[2])

        ############## other ##############
        header_class_end = "};"
        header_end = "\n#endif"

        header_classdef = self.make_method(f"ClassDef({self.name},0)", tab_no=1)#, omit_semicolon=True)
        source_classimp = self.make_method(f"ClassImp({self.name})")#, omit_semicolon=True)

        ############## join header ##############
        header_list = [
            header_define, header_container,
            header_include_root, header_include_lilak, header_include_other,
            "",header_description, header_class,
            header_class_public, header_constructor, header_destructor,
            "", header_clear, header_print, header_copy,
            "", header_getter,
            "", header_setter]
        if len(header_public_par.strip())>0:    header_list.extend(["", header_public_par])
        if len(header_protected_par.strip())>0: header_list.extend(["",header_class_protected, header_protected_par])
        if len(header_private_par.strip())>0:   header_list.extend(["",header_class_private, header_private_par])
        header_list.extend(["",header_classdef,header_class_end,header_end])
        header_all = '\n'.join(header_list)

        ############## join source ##############
        source_list = [
            source_include,
            "",source_classimp,
            "",source_constructor,
            "",source_clear,
            "",source_print,
            "",source_copy
            ]
        source_all = '\n'.join(source_list)

        ############## Par ##############
        par_all = '\n'.join(self.parfile_lines)

        ############## Print ##############
        name_full = os.path.join(self.path,self.name)

        if to_file:
            print(name_full)
            with open(f'{name_full}.h', 'w') as f1: print(header_all,file=f1)
            with open(f'{name_full}.cpp', 'w') as f1: print(source_all,file=f1)
            #with open(f'{name_full}.par', 'w') as f1: print(par_all,file=f1)

        if to_screen:
            print(f"{name_full}.h >>>>>")
            print(header_all)
            print(f"\n\n{name_full}.cpp >>>>>")
            print(source_all)


    def print_task(self,to_screen=False,to_file=True,print_example_comments=False):
        """Print header and source file of lilak task class content to screen or file

        to_screen (bool ; False) -- If True, print container to screen
        to_file (bool ; True) -- If True, print container to file ({path}/{name}.cpp, {path}/{name}.h) 
        print_example_comments (bool ; True) -- Print comments that helps you filling up reset of the class.
        """
        self.init_print()

        br1 = "{"
        br2 = "}"

        self.include_headers('TClonesArray.h')
        self.include_headers('LKLogger.h')
        self.include_headers('LKTask.h')
        self.include_headers('LKParameterContainer.h')
        self.include_headers('LKRun.h')
        self.include_headers('<iostream>')

        tab1 = ' '*(self.tab_size*1)
        tab2 = ' '*(self.tab_size*2)
        etab1 = '\n'+tab1
        etab2 = '\n'+tab2

        name_upper = self.name.upper()
        header_define = f"""#ifndef {name_upper}_HH
#define {name_upper}_HH
"""
        header_LKTask="""Remove this comment block after reading it through
Or use print_example_comments=False option to omit printing

# Example LILAK task class

## Essential
 - Write Init() method.
 - Write Exec() method using Clear() method to all clones arrays.
"""
        if print_example_comments:
            header_LKTask = self.make_doxygen_comment(header_LKTask,not_for_doxygen=True) + "\n"
        else:
            header_LKTask = ""
        header_include_lilak = '\n'.join(sorted(set(self.include_lilak_list)))
        header_include_root = '\n'.join(sorted(set(self.include_root_list)))
        header_include_other = '\n'.join(sorted(set(self.include_other_list)))
        header_description = self.make_doxygen_comment(self.comment)
        header_class = f"class {self.name} : public LKTask" + "\n{"

        source_include = f'#include "{self.name}.h"'

        ############## public ##############
        header_class_public = ' '*self.tab_size + "public:"
        constructor_content = ""
        header_constructor = self.make_method(self.name, tab_no=2, is_header=True)
        header_destructor = self.make_method("virtual ~"+self.name, tab_no=2, is_header=True)
        header_init = self.make_method("bool Init()", tab_no=2, is_header=True)
        header_exec = self.make_method("void Exec(Option_t *option)", tab_no=2, is_header=True)

        header_getter = tab2 + etab2.join(self.get_full_list[0])
        header_setter = tab2 + etab2.join(self.set_full_list[0])
        header_public_par = tab2 + etab2.join(self.par_def_list[0])

        self.par_init_list.insert(0,"//TODO Put intialization todos here which are not iterative job though event")
        self.par_init_list.insert(1,f'lk_info << "Initializing {self.name}" << std::endl;')
        self.par_init_list.insert(2,"")
        self.par_init_list.insert(3,"auto run = LKRun::GetRun();")
        self.par_init_list.insert(4,"auto par = run -> GetPar();")
        self.par_init_list.insert(5,"")
        init_content = '\n'.join(self.par_init_list)

        self.data_exec_list.insert(0,"//TODO Put the main task job here. Exec() method will be executed for every event.")
        self.data_exec_list.insert(1,"//All the Clear() methods of output data array are usually called at the start of the Exec()")
        self.data_exec_list.append("")
        self.data_exec_list.append(f'lk_info << "{self.name} container" << std::endl;')
        exec_content = '\n'.join(self.data_exec_list)

        source_constructor = self.make_method(f"{self.name}::{self.name}() {br1}{constructor_content}{br2}", 0, is_source=True)
        source_init = self.make_method(f"bool Init() {br1}{init_content}{br2}", 0, is_source=True)
        source_exec = self.make_method(f"void Exec(Option_t *option) const {br1}{exec_ontent}{br2}", 0, is_source=True)

        ############## protected ##############
        header_class_protected = ' '*self.tab_size + "protected:"
        header_protected_par = tab2 + etab2.join(self.par_def_list[1])

        ############## private ##############
        header_class_private = ' '*self.tab_size + "private:"
        header_private_par = tab2 + etab2.join(self.data_array_def_list)
        header_private_par = tab2 + etab2.join(self.par_def_list[2])

        ############## other ##############
        header_class_end = "};"
        header_end = "\n#endif"

        header_classdef = self.make_method(f"ClassDef({self.name},0)", tab_no=1)#, omit_semicolon=True)
        source_classimp = self.make_method(f"ClassImp({self.name})")#, omit_semicolon=True)

        ############## join header ##############
        header_list = [
            header_define, header_LKTask,
            header_include_root, header_include_lilak, header_include_other,
            "",header_description, header_class,
            header_class_public, header_constructor, header_destructor,
            "", header_init, header_exec,
            "", header_getter,
            "", header_setter]
        if len(header_public_par.strip())>0:     header_list.extend(["", header_public_par])
        if len(header_protected_par.strip())>0:  header_list.extend(["",header_class_protected, header_protected_par])
        if len(header_private_par.strip())>0:    header_list.extend(["",header_class_private, header_private_par])
        header_list.extend(["",header_classdef,header_class_end,header_end])
        header_all = '\n'.join(header_list)

        ############## join source ##############
        source_list = [
            source_include,
            "",source_classimp,
            "",source_constructor,
            "",source_init,
            "",source_exec,
            ]
        source_all = '\n'.join(source_list)

        ############## Par ##############
        par_all = '\n'.join(self.parfile_lines)

        ############## Print ##############
        name_full = os.path.join(self.path,self.name)

        
        if to_file:
            print(name_full)
            with open(f'{name_full}.h', 'w') as f1: print(header_all,file=f1)
            with open(f'{name_full}.cpp', 'w') as f1: print(source_all,file=f1)
            with open(f'{name_full}.par', 'w') as f1: print(par_all,file=f1)

        if to_screen:
            print(f"{name_full}.h >>>>>")
            print(header_all)
            print(f"\n\n{name_full}.cpp >>>>>")
            print(source_all)

if __name__ == "__main__":
    help(lilakcc)
