def break_function(func_full):
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
                    if   line.find("/** ")==0: line = line[4:]
                    elif line.find("/**")==0: line = line[3:]
                    if   line.find("/* ")==0: line = line[3:]
                    elif line.find("/*")==0: line = line[2:]
                    if   line.find("*/ ")==0: line = line[3:]
                    elif line.find("*/")==0: line = line[2:]
                    if   line.find("* ")==0: line = line[2:]
                    elif line.find("*")==0: line = line[1:]
                    func_prec_list.append(line)

    ib1 = func_noc.find("(")
    ic1 = func_noc.find("//")
    while ic1>=0 and ic1<ib1:
        ic2 = func_noc.find("\n")
        if ic1==func_noc.find("///"):
            func_linec = func_noc[ic1+3:ic2]
        else:
            func_linec = func_noc[ic1+2:ic2]
        func_noc = func_noc[ic2+1:]
        func_prec_list.append(func_linec)
        ib1 = func_noc.find("(")
        ic1 = func_noc.find("//")

    func_prec = '\n'.join(func_prec_list) if len(func_prec_list)!=0 else ""

    ib1 = func_noc.find("(")
    ib2 = func_noc.find(")")
    ib3 = func_noc.find("{")
    ib4 = func_noc.find("}")
    iname = func_noc[:ib1].rfind(" ")+1

    func_pstc = ""
    func_aft4 = func_noc[ib4+1:]
    ic3 = func_aft4.find("//")
    if ic3>=0:
        ic4 = func_aft4.find("///<")
        if ic4>=0:
            func_pstc = func_aft4[ic4+4:]
        else:
            func_pstc = func_aft4[ic3+2:]
    func_pstc = func_pstc.strip()

    func_name = func_noc[iname:ib1]
    func_type = func_noc[:iname-1]
    func_parameters = func_noc[ib1+1:ib2]
    func_content = func_noc[ib3+1:ib4]
    is_const = True if func_noc[ib2+1:ib3].find("const") else False
    if func_content[0]=="\n": func_content = func_content[1:]
    if func_content[len(func_content)-1]=="\n": func_content = func_content[:len(func_content)-1]
    #print("func_noc: ",func_noc)

    print("func_prec: ",func_prec)
    print("func_pstc: ",func_pstc)
    print("func_type: ",func_type)
    print("func_name: ",func_name)
    print("func_parameters: ",func_parameters.strip())
    print("func_content: ",func_content)
    print("is_const: ",is_const)

break_function("""///This is the 1st comment
///This is the 2nd comment
///This is the 3rd comment
///This is the 4th comment
///  - This is spaced comment
///  - This is spaced comment
///  - This is spaced comment
///  - This is spaced comment
///
///This is the 5th comment
///This is the 6th comment
///This is the 7th comment
///This is the 8th comment
///
virtual void LKExampleContainer::FunctionName(These *are, input parameters)
{
    This is content1;
    This is content2;
    This is content3;
    This is content4;
} // this is post comment"""
)

#break_function("""
#/*
# * This is the 1st comment
# * This is the 2nd comment
# * This is the 3rd comment
# * This is the 4th comment
# *   - This is spaced comment
# *   - This is spaced comment
# *   - This is spaced comment
# *   - This is spaced comment
# */
#/**
# * This is the 5th comment
# * This is the 6th comment
# * This is the 7th comment
# * This is the 8th comment
# */
#virtual void LKExampleContainer::FunctionName(These *are, input parameters)
#{
#    This is content;
#} // this is post comment"""
#)

#break_function("""virtual void LKExampleContainer::FunctionName(These *are, input parameters) const { This is content0; } ///< bla bla bla""")
