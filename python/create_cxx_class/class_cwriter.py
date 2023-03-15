import os

class cwriter:
    """Write c++ class with source and header """
    def __init__(self):
        self.name = "LKExampleContainer"
        self.path = ""
        self.description = ""
        self.par_clear_list = []
        self.par_print_list = []
        self.par_copy_list = []
        self.par_full_list = [[],[],[]]
        self.set_full_list = [[],[],[]]
        self.get_full_list = [[],[],[]]
        self.include_root_list = []
        self.include_lilak_list = []
        self.include_other_list = []
        self.tab_size = 2
  
    def set_name(self,name):
        """Set name of the class"""
        self.name = name
  
    def set_file_path(self,path):
        """Set path where files are created"""
        self.path = path

    def set_description(self, description):
        """Description of the class"""
        self.description = description 

    def set_tab_size(tab_size):
        """Set tab size"""
        self.tab_size = tab_size

    def separate_comments(self,func_full):
        func_noc = func_full
        func_prec_list = []

        ic1 = func_noc.find("/*")
        while ic1>=0:
            ic2 = func_noc.find("*/")
            func_foundblock = func_noc[ic1:ic2+2]
            func_noc = func_noc[ic2+3:]
            ic1 = func_noc.find("/*")
            if func_foundblock.isspace()==False:
                for line in func_foundblock.splitlines():
                    line = line.strip()
                    if line!="/**" and line!="*/" and line!="/*":
                        if   line.find("/** ")==0:  line = line[4:]
                        elif line.find("/**")==0:   line = line[3:]
                        if   line.find("/* ")==0:   line = line[3:]
                        elif line.find("/*")==0:    line = line[2:]
                        if   line.find("*/ ")==0:   line = line[3:]
                        elif line.find("*/")==0:    line = line[2:]
                        if   line.find("* ")==0:    line = line[2:]
                        elif line.find("*")==0:     line = line[1:]
                        func_prec_list.append(line)

        ib1 = func_noc.find("(")
        ic1 = func_noc.find("//")
        while ic1>=0 and ic1<ib1:
            ic2 = func_noc.find("\n")
            if ic1==func_noc.find("///"):   func_linec = func_noc[ic1+3:ic2]
            else:                           func_linec = func_noc[ic1+2:ic2]
            func_noc = func_noc[ic2+1:]
            func_prec_list.append(func_linec)
            ib1 = func_noc.find("(")
            ic1 = func_noc.find("//")

        func_prec = '\n'.join(func_prec_list) if len(func_prec_list)!=0 else ""

        ib1 = func_noc.find("(")
        if ib1<0: ib1 = len(func_noc)
        ispace = func_noc[:ib1].rfind(" ")
        while ispace==ib1-1:
            func_noc = func_noc[:ispace]+func_noc[ib1:]
            ib1 = func_noc.find("(")
            if ib1<0: ib1 = len(func_noc)
            ispace = func_noc[:ib1].rfind(" ")

        if ispace<0: iname = 0
        else: iname = ispace + 1

        ib2 = func_noc.rfind(")")
        if ib2<0: ib2 = len(func_noc)

        ib3 = func_noc.find("{")
        ib4 = func_noc.find("}")

        func_pstc = ""
        if ib4<0: func_aft4 = func_noc[ib2+1:]
        else:     func_aft4 = func_noc[ib4+1:]
        ic3 = func_aft4.find("//")
        if ic3>=0:
            ic4 = func_aft4.find("///<")
            if ic4>=0: func_pstc = func_aft4[ic4+4:]
            else:      func_pstc = func_aft4[ic3+2:]
        func_pstc = func_pstc.strip()

        func_name = func_noc[iname:ib1]
        if iname>0: func_type = func_noc[:iname-1]
        else: func_type = ""

        func_parameters = func_noc[ib1+1:ib2]
        if ib3>0:
            func_content = func_noc[ib3+1:ib4]
            func_is_const = True if func_noc[ib2+1:ib3].find("const")>=0 else False
            if func_content[0]=="\n": func_content = func_content[1:]
            if func_content[len(func_content)-1]=="\n": func_content = func_content[:len(func_content)-1]
        else:
            func_content = ""
            func_is_const = True if func_noc[ib2+1:].find("const")>=0 else False

        func_prec_list.append(func_pstc)
        func_comment = '\n'.join(func_prec_list)

        tab_no = 0 #todo

        return func_type, func_name, func_parameters, func_content, tab_no, func_comment, func_is_const

    def make_function(self, func_type, func_name, func_parameters, func_content="", tab_no=0, func_comment="", func_is_const=False, is_header=False, is_source=False, omit_semicolon=False, in_line=False):
        """Make c++ function with given parameters

        func_type       (string) -- data type of function
        func_name       (string) -- name of the function
        func_parameters (string) -- input parameters of function
        func_content    (string; "") -- content of the function
        tab_no          (string ; 0) -- number of tabs (indents) of the function
        func_comment    (string ; "") -- comment of the function
        func_is_const   (bool ; False) -- Put const after the function definition
        is_header       (bool ; False) -- Make header file
        is_source       (bool ; False) -- Make source file
        in_line         (bool ; False) -- Make function in-line
        omit_semicolon  (bool ; False) -- Omit ";"
        """
        if is_source and func_name.find("::")<0: func_full = self.name + "::" + func_name + "(" + func_parameters + ")"
        else:                                    func_full = func_name + "(" + func_parameters + ")"

        if len(func_type)>0: func_full = ' '*(self.tab_size*tab_no) + func_type + " " + func_full
        else:                func_full = ' '*(self.tab_size*tab_no) + func_full

        if (func_is_const):
            func_full = func_full + " const"

        lines = func_content.split('\n')

        just_define = False
        mult_line = False
        if in_line==True: pass
        elif is_header:             just_define = True
        elif is_source:             mult_line = True
        elif len(func_content)==0:  just_define = True
        else:                       mult_line = True

        if just_define:
            if omit_semicolon==False:
                func_full = func_full + ";"
        elif mult_line:
            if func_content=="":
                func_full = func_full + '\n' + ' '*(self.tab_size*tab_no) + "{"
                func_full = func_full + '\n' + ' '*(self.tab_size*tab_no) + "}"
            else:
                for i in range(len(lines)):
                    lines[i] = ' '*(self.tab_size*(tab_no+1)) + lines[i]
                func_full = func_full + '\n' + ' '*(self.tab_size*tab_no) + "{"
                func_full = func_full + '\n' + '\n'.join(lines)
                func_full = func_full + '\n' + ' '*(self.tab_size*tab_no) + "}"
        else:
            if func_content.isspace():  func_full =  func_full + " {}"
            else:                       func_full =  func_full + " { " + func_content + " }"
        return self.make_doxygen_comment(func_comment, func_full)

  
    def make_fline(self, func_full, func_comment="", tab_no=-1, is_source=False, is_header=False, omit_semicolon=False, in_line=False):
        """ Make funciton from line"""
        func_type, func_name, func_parameters, func_content, tab_no2, func_comment2, func_is_const = self.separate_comments(func_full)

        if   len(func_comment)==0 and len(func_comment2)!=0: func_comment = func_comment2
        elif len(func_comment)!=0 and len(func_comment2)==0: pass
        elif len(func_comment)!=0 and len(func_comment2)!=0: func_comment = func_comment + '\n' + func_comment2

        if   tab_no<-1 and tab_no2>=0: tab_no = tab_no2
        elif tab_no>=0: tab_no = tab_no
        else: tab_no = 0

        return self.make_function(func_type, func_name, func_parameters, func_content, tab_no, func_comment, func_is_const, is_header, is_source, omit_semicolon, in_line)

    def make_doxygen_comment(self, comment, add_to="", always_mult_line=False, not_for_doxygen=False):
        """Make doxygen comment

        add_to (string) -- If add_to parameter is set True, comment will be put after (before)
                           for the case comment is one-line (multi-line) and return it.
                           Return just comment if add_to is set False. 
        always_mult_line (bool) -- The comments are assumed that it is multi-line and use /** [...] */
        not_for_doxygen (bool) -- If True: /** -> /*, ///< -> //
        """
        if len(comment)==0:
            if len(add_to)>0: return add_to
            else:             return ""
        else:
            if always_mult_line or "\n" in comment or "\r\n" in comment:
                lines = comment.split('\n')
                for i in range(len(lines)):
                    lines[i] = ' * ' + lines[i]
                else:
                    if (not_for_doxygen): lines.insert(0,"/*")
                    else:                 lines.insert(0,"/**")
                    lines.append(" */")
                comment = '\n'.join(lines)
                if len(add_to)>0: return comment + add_to
                else:             return comment
            else:
                comment = " ///< " + comment;
                if len(add_to)>0: return add_to + comment
                else:             return comment

    def include_headers(self,headers):
        """Include header files assuming that headers are separated by spaces or line-break"""
        if len(headers)==0:
            return
        header_list = headers.replace(' ','\n')
        header_list = headers.split('\n')
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

    def add_par(self,ppp_index,
                par_type, par_name, par_init, par_comment="", par_name_lc="",
                set_type="", set_name="", set_comment="",
                get_type="", get_name="", get_comment="", get_is_const=True,
                headers="", use_fpar=True):
        """ Add parameter

        ppp_index    (int) -- 0: public, 1: protected, 2: private.
        par_type     (string) -- Type of parameter
        par_name     (string) -- Name of parameter
        par_init     (string ; "") -- Initial parameter value. If par_init is empty string(""), it will not be initialized
                                      However it is highly recommended that to give initial parameter value to a value that is unlikely to be given.
                                      This will help you in debugging in the analysis step.
        par_name_lc  (string ; "") -- Local parameter name. By defualt, = par_name or par_name + "_"
        par_comment  (string ; "") -- Comment to parameter.
        set_type     (string ; "") -- Setter input type. By defualt, = par_type
        set_name     (string ; "") -- Setter name. By defualt, = Set + par_name[0].title()+par_name[1:]
        set_comment  (string ; "") -- Comment to setter
        get_type     (string ; "") -- Getter type. By defualt, = par_type
        get_name     (string ; "") -- Getter name. By defualt, = Get + par_name[0].title()+par_name[1:]
        get_comment  (string ; "") -- Comment to getter
        get_is_const (bool ; True) -- Set True if getter is const
        headers      (string ; "") -- Headers to include (separated by space of line-break)
        use_fpar     (bool ; True) -- By default, field (or member) parameter name will be set to
                                      "f" + par_name[0].title()+par_name[1:]. Set use_fpar to False if you wish
                                      to use par_name itself.
        """
        ############ field parameter name ############
        if use_fpar: par_name_field = "f" + par_name[0].title()+par_name[1:]
        else:        par_name_field = par_name

        ############ parameter definition ############
        par_clear = par_name_field
        if len(par_init)>0:
            par_clear = par_clear + " = " + par_init;
        par_clear = par_clear + ";"
        par_full = par_type + " " + par_clear
        par_full = self.make_doxygen_comment(par_comment,par_full)

        ############ parameter print ############
        par_print = f'lx_info << "{par_name} : " << {par_name_field} << std::endl;'

        ############ local parameter name ############
        if len(par_name_lc)==0:
            par_name_lc = par_name
            if par_name_lc==par_name_field:
                par_name_lc = par_name_lc + "_"

        ############ settter definition ############
        if len(set_type)==0: set_type = par_type
        if len(set_name)==0: set_name = "Set" + par_name[0].title()+par_name[1:]
        set_full = self.make_function("void", set_name, f"{set_type} {par_name_lc}", f"{par_name_field} = {par_name_lc};", 0, set_comment, in_line=True)
  
        ############ gettter definition ############
        if len(get_type)==0: get_type = par_type
        if len(get_name)==0: get_name = "Get" + par_name[0].title()+par_name[1:]
        #get_full = self.make_function(get_type, get_name, "", f"return {par_name_field};", 0, get_comment, func_is_const=get_is_const, in_line=True)
        get_full = self.make_fline(f"{get_type} {get_name}() const " +"{"+ f"return {par_name_field};"+"}", in_line=True)
  
        ############ parameter copy ############
        #par_copy = self.make_function("","objCopy."+set_name, f"{par_name_field}", "", 0, "")
        par_copy = self.make_fline(f"objCopy.{set_name}({par_name_field})")

        ############ gettter definition ############
        self.par_clear_list.append(par_clear);
        self.par_print_list.append(par_print);
        self.par_copy_list.append(par_copy);
        self.par_full_list[ppp_index].append(par_full);
        self.set_full_list[0].append(set_full);
        self.get_full_list[0].append(get_full);

        ############ include headers ############
        self.include_headers(headers)
  
    def add_public_par(self,
                par_type, par_name, par_init, par_comment="", par_name_lc="",
                set_type="", set_name="", set_comment="",
                get_type="", get_name="", get_comment="", get_is_const=True,
                headers="", use_fpar=True):
        self.add_par(0,
                par_type, par_name, par_init, par_comment, par_name_lc,
                set_type, set_name, set_comment,
                get_type, get_name, get_comment, get_is_const,
                headers, use_fpar)

    def add_protected_par(self,
                par_type, par_name, par_init, par_comment="", par_name_lc="",
                set_type="", set_name="", set_comment="",
                get_type="", get_name="", get_comment="", get_is_const=True,
                headers="", use_fpar=True):
        self.add_par(1,
                par_type, par_name, par_init, par_comment, par_name_lc,
                set_type, set_name, set_comment,
                get_type, get_name, get_comment, get_is_const,
                headers, use_fpar)

    def add_private_par(self,
                par_type, par_name, par_init, par_comment="", par_name_lc="",
                set_type="", set_name="", set_comment="",
                get_type="", get_name="", get_comment="", get_is_const=True,
                headers="", use_fpar=True):
        self.add_par(2,
                par_type, par_name, par_init, par_comment, par_name_lc,
                set_type, set_name, set_comment,
                get_type, get_name, get_comment, get_is_const,
                headers, use_fpar)

    def print_container(self,to_screen=False,to_file=True,print_example_comments=True):
        """Print header and source file content to screen or file

        to_screen (bool ; False) -- If True, print container to screen
        to_file (bool ; True) -- If True, print container to file ({path}/{name}.cc, {path}/{name}.hh) 
        print_example_comments (bool ; True) -- Print comments that helps you filling up reset of the class.
        """
        self.include_headers('TClonesArray.h')
        self.include_headers('LKLogger.h')
        self.include_headers('LKContainer.h')
        #self.include_headers('LKParameterContainer.h')
        #self.include_headers('LKRun.h')
        self.include_headers('<iostream>')

        tab1 = ' '*(self.tab_size*1)
        tab2 = ' '*(self.tab_size*2)
        etab1 = '\n'+tab1
        etab2 = '\n'+tab2

        name_upper = self.name.upper()
        header_define = f"""#ifndef {name_upper}_HH
#define {name_upper}_HH
"""
        header_LKContainer="""Remove this comment block after reading it through
Or use print_example_comments=False option to omit printing

# Example LILAK container class

## Essential component: 
 - inherit LKContainer as public.
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

## Recommended component:
 - Documentaion like this!
 - Write Print() to see what is inside the container;

## If you have time
 - Write Copy() for copying object
"""
        if print_example_comments:
            header_LKContainer = self.make_doxygen_comment(header_LKContainer,not_for_doxygen=True) + "\n"
        else:
            header_LKContainer = ""
        header_include_lilak = '\n'.join(sorted(set(self.include_lilak_list)))
        header_include_root = '\n'.join(sorted(set(self.include_root_list)))
        header_include_other = '\n'.join(sorted(set(self.include_other_list)))
        header_description = self.make_doxygen_comment(self.description)
        header_class = f"class {self.name} : public LKContainer" + "\n{"

        source_include = f'#include "{self.name}.hh"'

        ############## public ############## 
        header_class_public = ' '*self.tab_size + "public:"
        if print_example_comments:
            constructor_content = "// It is essential to place Clear() method inside the constructor for TClonesArray feature.\nClear();"
        else:
            constructor_content = "Clear();"
        header_constructor = self.make_fline(self.name, tab_no=2, is_header=True)
        header_destructor = self.make_fline("virtual ~"+self.name, tab_no=2, is_header=True)
        header_clear = self.make_fline("virtual void Clear(Option_t *option)", tab_no=2, is_header=True)
        header_print = self.make_fline("virtual void Print(Option_t *option) const;", tab_no=2, is_header=True)
        header_copy = self.make_fline("virtual void Copy (TObject &object) const;",  tab_no=2, is_header=True)
        header_getter = tab2 + etab2.join(self.get_full_list[0])
        header_setter = tab2 + etab2.join(self.set_full_list[0])
        header_public_par = tab2 + etab2.join(self.par_full_list[0])

        clear_content = '\n'.join(self.par_clear_list)
        self.par_print_list.insert(0,"//TODO You will probability need to modify here")
        self.par_print_list.insert(1,f'lx_info << "{self.name} container" << std::endl;')
        print_content = '\n'.join(self.par_print_list)
        self.par_copy_list.insert(0,"//TODO You should copy data from this container to objCopy")
        self.par_copy_list.insert(1,"LKContainer::Copy(object);")
        self.par_copy_list.insert(2,f"auto objCopy = ({self.name} &) object;")
        copy_content = '\n'.join(self.par_copy_list)
        source_constructor = self.make_function("", self.name, "", constructor_content, 0, is_source=True)
        source_clear = self.make_function("void", "Clear", "Option_t *option", clear_content, 0, is_source=True)
        source_print = self.make_function("void", "Print", "Option_t *option", print_content, 0, "", True, is_source=True)
        source_copy = self.make_function ("void", "Copy",  "TObject &object",  copy_content, 0, "", True, is_source=True)

        ############## protected ############## 
        header_class_protected = ' '*self.tab_size + "protected:"
        header_protected_par = tab2 + etab2.join(self.par_full_list[1])

        ############## private ############## 
        header_class_private = ' '*self.tab_size + "private:"
        header_private_par = tab2 + etab2.join(self.par_full_list[2])

        ############## other ############## 
        header_class_end = "};"
        header_end = "\n#endif"

        header_classdef = self.make_fline(f"ClassDef({self.name},0)", omit_semicolon=True)
        source_classimp = self.make_fline(f"ClassImp({self.name})", omit_semicolon=True)

        ############## join header ############## 
        header_list = [header_define, header_LKContainer,
            header_include_root, header_include_lilak, header_include_other,
            "",header_description, header_class,
            header_class_public, header_constructor, header_destructor,
            "", header_clear, header_print, header_copy,
            "", header_getter, "", header_setter]
        if (len(header_public_par.strip())>0): header_list.extend(["", header_public_par])
        if header_protected_par.strip():       header_list.extend(["",header_class_protected, header_protected_par])
        if header_private_par.strip():         header_list.extend(["",header_class_private, header_private_par])
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

        ############## Print ############## 
        name_full = os.path.join(self.path,self.name)

        if to_file:
            print(name_full)
            with open(f'{name_full}.hh', 'w') as f1: print(header_all,file=f1)
            with open(f'{name_full}.cc', 'w') as f1: print(source_all,file=f1)

        if to_screen:
            print(f"{name_full}.hh >>>>>")
            print(header_all)
            print(f"\n\n{name_full}.cc >>>>>")
            print(source_all)
