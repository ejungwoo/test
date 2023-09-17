import os
import json

class bib_manager:

    def __init__(self, bibtex_input):
        self.print_process = False
        self.init()
        self.read_bibtex(bibtex_input)

    def init(self):
        self.clear()
        self.journal_list = [] # should not be inside the clear method
        self.required_fields = {}
        self.optional_fields = {}
        self.read_list_of_journals()
        self.read_list_of_entry_types()

    def clear(self):
        self.bib_fields = {}
        self.author1 = []
        self.author_list = []

    def read_list_of_entry_types(self):
        f1 = open('data/common/list_of_entry_types','r')
        new_type = True
        following_is_required_fields = False
        following_is_optional_fields = False
        type_name = ""
        type_equal_to = ""
        line_required = ""
        line_optional = ""
        while True:
            line = f1.readline()
            if not line: break
            line = line.strip()
            if len(line)==0:
                new_type = True
                if len(type_name)>0:
                    line_required = line_required.strip()
                    line_optional = line_optional.strip()
                    self.required_fields[type_name] = []
                    self.optional_fields[type_name] = []
                    if len(type_equal_to)>0:
                         self.required_fields[type_name] = self.required_fields[type_equal_to] 
                         self.optional_fields[type_name] = self.optional_fields[type_equal_to] 
                    else:
                        for field in line_required.split(","):
                            if field.find("/")>=0: field = field[:field.find("/")]
                            self.required_fields[type_name].append(field.strip())
                        for field in line_optional.split(","):
                            if field.find("/")>=0: field = field[:field.find("/")]
                            self.optional_fields[type_name].append(field.strip())
                    #print()
                    #print(f"@{type_name}")
                    #for field in self.required_fields[type_name]: print(field)
                    #for field in self.optional_fields[type_name]: print(f"*{field}")
                type_name = ""
                type_equal_to = ""
                line_required = ""
                line_optional = ""
                following_is_required_fields = False
                following_is_optional_fields = False
                continue
            elif new_type:
                type_name = line
                new_type = False
                continue
            elif line[0]=='*':
                type_equal_to = line[1:]
                continue
            elif line[:16]=="Required fields:":
                following_is_required_fields = True
                following_is_optional_fields = False
                line = line[16:]
            elif line[:16]=="Optional fields:":
                following_is_optional_fields = True
                following_is_required_fields = False
                line = line[16:]
            if following_is_required_fields: line_required = line_required + line
            if following_is_optional_fields: line_optional = line_optional + line

    def read_list_of_journals(self):
        with open('data/common/list_of_journals','r') as f1:
            lines = f1.readlines()
            for line in lines:
                line = line.strip()
                full_name, minimum_name, short_name = line.split('/')
                full_name, minimum_name, short_name = full_name.strip(), minimum_name.strip(), short_name.strip()
                if self.print_process: print(f"{full_name} / {minimum_name} / {short_name}")
                if len(full_name)>0:
                    self.journal_list.append([full_name, minimum_name, short_name])

    def read_bibtex(self, bibtex_input):
        if len(bibtex_input)==0:
            bibtex_input = input("enter bibtext content: ")
        f1 = open(bibtex_input,'r')
        lines = f1.read()
        while True:
            if len(lines)==0:
                print(f'********** WARNING! content is empty! **********')
                break
            if self.print_process:
                print(f"\n\n#####################################################")
                print(lines)
                print(f"#####################################################")
            self.clear()
            iaa = lines.find("@")
            if iaa<0:
                print(f'********** WARNING! cannot find @! **********')
                break
            ibr1 = lines.find("{")
            icomma = lines.find(",")
            self.make_type(lines[iaa+1:ibr1])
            self.bib_fields["oldname"] = lines[ibr1+1:icomma]
            found_aa = False
            lines = lines[icomma+1:]
            while True:
                lines, entry_title, entry_value = self.find_next_entry(lines)
                entry_title = entry_title.lower()
                if entry_title=="": break
                if entry_title=='"': continue
                if entry_title=="@":
                    found_aa = True
                    break
                self.make_field(entry_title, entry_value)
                if self.print_process:
                    line_example = lines
                    if len(line_example)>19:
                        line_example = lines[:20].strip() + " ..."
                    print(f"#################### lines : {line_example}")
                    print(f"#################### entry : {entry_title} >> {entry_value}")
            self.finalize_bib()
            self.confirm_entry()
            self.write_entry()
            if found_aa==False:
                break

    def print_key(self, key, idx=-1):
        if idx>=0:
            print(f"{idx:>2}. {key:20}{self.bib_fields[key]}")
        else:
            print(f"+{key:20}{self.bib_fields[key]}")

    def write_entry(self):
        if "bibname" in self.bib_fields:
            file_name_json = f'data/json/{self.bib_fields["bibname"]}.json'
            with open(file_name_json,'w') as file_json:
                print(f'writting {file_name_json}')
                json.dump(self.bib_fields,file_json)
                file_json.close()
        if "numbering" in self.bib_fields:
            max_number = -1
            files_in_directory = os.listdir("data/numbering")
            for file_name in files_in_directory:
                try:
                    file_number = int(file_name.split('_')[0])
                    if file_number>max_number:
                        max_number = file_number
                except (ValueError, IndexError):
                    pass
            next_number = max_number + 1
            file_name_numbering = f'data/numbering/{next_number}_{self.bib_fields["bibname"]}'
            with open(file_name_numbering,'w') as file_numbering:
                print(f'touch {file_name_numbering}')
                pass
        if "collaboration" in self.bib_fields:
            directory_path = f'data/collaboration'
            if self.bib_fields["collaboration"]:
                directory_path = directory_path + f'/{self.bib_fields["collaboration"]}'
                os.makedirs(directory_path, exist_ok=True)
                file_name_collaboration = f'{directory_path}/{self.bib_fields["bibname"]}'
                with open(file_name_collaboration,'w') as file_collaboration:
                    print(f'touch {file_name_collaboration}')
                    pass
        if "bibtag" in self.bib_fields:
            for tag1 in self.bib_fields["bibtag"]:
                if not tag1: continue
                directory_path = f'data/tag/{tag1}'
                os.makedirs(directory_path, exist_ok=True)
                file_name_tag1 = f'{directory_path}/{self.bib_fields["bibname"]}'
                with open(file_name_tag1,'w') as file_tag1:
                    print(f'touch {file_name_tag1}')
                    pass


        #file_name_list = f'list/{self.bib_fields["bibname"]}'
        #with open(file_name_json, 'r') 
        #    bib_fields2 = json.load(f3)
        #    print(bib_fields2)
        #    for key_name in bib_fields2:
        #        self.print_key(key_name)#,file=f2)

    def confirm_entry(self):
        self.make_bib_name()
        print(f'+++ {self.bib_fields["bibname"]}  ({self.bib_fields["oldname"]})')
        list_of_keys = []
        for key_name in self.bib_fields:
            self.print_key(key_name,len(list_of_keys))
            list_of_keys.append(key_name)
        question = f"==  Type number of entry to modify the content. Type enter if non: "
        while True:
            user_input = input(question)
            if user_input:
                key_name = list_of_keys[int(user_input)]
                if user_input.isdigit() and int(user_input)>=0 and int(user_input)<len(list_of_keys):
                    self.print_key(key_name)
                    question2 = f"==  Type value for {key_name}: "
                    user_value = input(question2)
                    if user_value:
                        self.make_field(key_name,user_value)
                    else:
                        break
                else:
                    print("out of index!")
                    #break
            else:
                break
        self.make_bib_name()

    def finalize_bib(self):
        bib_is_arxiv = False
        if self.bib_fields["bibtype"]=="inproceedings":
            if "archiveprefix" in self.bib_fields:
                bib_is_arxiv = True
        #__TECHINAL_REPORT_______________________________
        if self.bib_fields["bibtype"]=="techreport":
            if "reportnumber" in self.bib_fields:
                self.bib_fields["volume"] = self.bib_fields["reportnumber"].replace("-","")
            else:
                self.bib_fields["volume"] = ""
            if "institution" in self.bib_fields:
                institution = self.bib_fields["institution"].replace("-","")
                self.make_journal(institution,True)
            else:
                self.make_journal("Techical Report")
            self.bib_fields["page1"] = ""
        #__ARXIV_________________________________________
        elif self.bib_fields["bibtype"]=="misc" or bib_is_arxiv:
            key_contain_arxiv = ("archiveprefix" in self.bib_fields)
            url_contain_arxiv = False
            if "url" in self.bib_fields:
                url_contain_arxiv = (self.bib_fields["url"].find("arxiv.org")>=0)
            if key_contain_arxiv or url_contain_arxiv:
                self.make_journal("Arxiv")
                eprint = self.bib_fields["eprint"]
                if eprint.find("/")>=0:
                    self.bib_fields["volume"] = eprint.split("/")[0]
                    self.bib_fields["page1"] = eprint.split("/")[1]
                elif eprint.find("_")>=0:
                    self.bib_fields["volume"] = eprint.split("_")[0]
                    self.bib_fields["page1"] = eprint.split("_")[1]
                elif eprint.find(".")>=0:
                    self.bib_fields["volume"] = eprint.split(".")[0]
                    self.bib_fields["page1"] = eprint.split(".")[1]
                self.bib_fields["volume"] = self.bib_fields["volume"].replace("-","")
            else:
                self.make_journal("MISC",True)
                self.bib_fields["volume"] = ""
                self.bib_fields["page1"] = ""
        #__THESIS________________________________________
        elif self.bib_fields["bibtype"]=="phdthesis":
            self.make_journal("Thesis",True)
            self.bib_fields["volume"] = ""
            self.bib_fields["page1"] = ""

    def find_next_entry(self, lines):
        entry_title = ""
        entry_value = ""
        iaa = lines.find("@")
        ieq = lines.find("=")
        ibr1 = lines.find("{")
        if iaa>=0 and ieq>=0 and ibr1>=0 and iaa<ibr1 and iaa<ieq:
            return lines, "@", "@"
        entry_title = lines[:ieq].strip()
        lines = lines[ieq+1:]
        inside_bracket = 0
        inside_dbquote = False
        found_init_notation = False
        init_notation_is_bracket = False
        init_notation_is_dbquote = False
        meet_special_command = 1
        signal_end_of_value = False
        count_word_c = 0
        count_all_c = 0
        prev_c = ""
        for curr_c in lines:
            count_all_c = count_all_c + 1
            #if curr_c==',' and count_word_c>1:
            #    break
            #el
            if signal_end_of_value:
                if curr_c==',': break
                elif curr_c==' ' or curr_c=="\n": continue
                else:
                    break
                    count_all_c = count_all_c - 1
            elif curr_c=='\\':
                meet_special_command = 0
            elif meet_special_command==0:
                meet_special_command = meet_special_command + 1
            elif curr_c=='{':
                inside_bracket = inside_bracket + 1
                if found_init_notation==False:
                    init_notation_is_bracket = True
            elif curr_c=='}':
                inside_bracket = inside_bracket - 1
                if init_notation_is_bracket and inside_bracket==0:
                    signal_end_of_value = True
            elif curr_c=='"':
                if meet_special_command==1 and prev_c=='"':
                    meet_special_command + 1
                else:
                    if found_init_notation==False:
                        found_init_notation = True
                        init_notation_is_bracket = True
                    if inside_dbquote:
                        inside_dbquote = False
                    else:
                        inside_dbquote = True
                    if init_notation_is_bracket and inside_dbquote==False:
                        signal_end_of_value = True
            else:
                count_word_c = count_word_c + 1
            prev_c = curr_c
            entry_value = entry_value + curr_c
        lines = lines[count_all_c:]
        if signal_end_of_value==False:
            return lines, "", ""
        entry_value = entry_value.strip()
        if len(entry_value)>0:
            if entry_value[-1]==',': entry_value = entry_value[:-1].strip()
            if entry_value[0]=='{':  entry_value = entry_value[1:].strip()
            if entry_value[-1]=='}': entry_value = entry_value[:-1].strip()
        return lines, entry_title, entry_value

    def make_bib_name(self):
        name = self.make_nospace_author_name(self.author1)
        colb = self.bib_fields["collaboration"]
        jour = self.bib_fields["journal"][1]
        year = self.bib_fields["year"]
        volm = self.bib_fields["volume"]
        page = self.bib_fields["page1"]
        btag = self.bib_fields["bibtag"][0]
        if len(name)>0: name = name + "_"
        if len(colb)>0: colb = colb + "_"
        if len(jour)>0: jour = jour + "_"
        if len(year)>0: year = "y" + year + "_"
        if len(volm)>0: volm = "v" + volm + "_"
        if len(page)>0: page = "p" + page + "_"
        if len(btag)>0: btag = btag + "_"
        bib_name_new = name + colb + jour + year + volm + page + btag
        bib_name_new = bib_name_new[:-1]
        self.bib_fields["bibname"] = bib_name_new
        return bib_name_new

    def make_nospace_author_name(self, author):
        first_name  = author[0].replace(".","").strip().title()
        middle_name = author[1].replace(".","").strip().title()
        last_name   = author[2].replace(".","").strip().title()
        return last_name+first_name+middle_name

    def make_school(self, entry_value):
        self.bib_fields["school"] = entry_value
        self.bib_fields["institute"] = entry_value
        pass

    def make_doi(self, entry_value):
        self.bib_fields["doi"] = entry_value

    def make_bibtag(self, entry_value):
        for tag1 in entry_value.split(','):
            tag1 = tag1.strip()
            if not tag1:
                continue
            if self.bib_fields["bibtag"][0]=='':
                self.bib_fields["bibtag"][0] = tag1
            else:
                self.bib_fields["bibtag"].append(tag1)

    def make_archivePrefix(self, entry_value):
        self.make_journal("Arxiv")

    def make_journal(self, entry_value, register_temporarily=False):
        if register_temporarily:
            journal1 = entry_value.strip()
            journal2 = entry_value.strip()
            journal3 = entry_value.strip()
            if journal2.find(" ")>=0:
                split_journal2 = journal2.split()
                journal2 = ""
                for token_journal2 in split_journal2:
                    journal2 = journal2 + token_journal2[0].upper()
            print(f'NOTE! The journal "{entry_value}" will be added temporarily: {journal1} / {journal2} / {journal3}')
            self.bib_fields["journal"] = [journal1,journal2,journal3]
        elif len(entry_value)>0:
            found_etnry = False
            for journal_entry in self.journal_list:
                if journal_entry[0]==entry_value:
                    self.bib_fields["journal"] = journal_entry
                    found_etnry = True
                    break
            if found_etnry==False:
                print(f'********** WARNING! Add journal "{entry_value}" to journal list! **********')
                exit()
        if self.print_process: print(f'#################### journal : {self.bib_fields["journal"][0]}  /  {self.bib_fields["journal"][1]}  /  {self.bib_fields["journal"][2]}')

    def make_pages(self, entry_value):
        self.bib_fields["pages"] = entry_value
        self.bib_fields["page1"] = ""
        self.bib_fields["page2"] = ""
        if entry_value.find("--")>=0:
            self.bib_fields["page1"] = entry_value.split("--")[0]
            self.bib_fields["page2"] = entry_value.split("--")[1]
        elif entry_value.find("-")>=0:
            self.bib_fields["page1"] = entry_value.split("-")[0]
            self.bib_fields["page2"] = entry_value.split("-")[1]
        else:
            self.bib_fields["page1"] = entry_value
            self.bib_fields["page2"] = 0
        if self.print_process: print(f'#################### pages : {self.bib_fields["page1"]} - {self.bib_fields["page2"]}')

    def make_type(self, entry_value):
        type_name = entry_value
        self.bib_fields["bibname"] = ""
        self.bib_fields["bibnumber"] = -1
        self.bib_fields["bibtype"] = type_name
        self.bib_fields["bibtag"] = [""]
        self.bib_fields["collaboration"] = ""
        self.bib_fields["oldname"] = ""
        if type_name in self.required_fields:
            for field in self.required_fields[type_name]:
                self.bib_fields[field] = ""
        else:
            print(f'********** WARNING! Add type "{type_name}" to type list! **********')

    def make_field(self, entry_title, entry_value):
        if   entry_title=="author"  : self.make_author_list(entry_value)
        elif entry_title=="journal" : self.make_journal(entry_value)
        elif entry_title=="school"  : self.make_school(entry_value)
        elif entry_title=="pages"   : self.make_pages(entry_value)
        elif entry_title=="doi"     : self.make_doi(entry_value)
        elif entry_title=="bibtag"  : self.make_bibtag(entry_value)
        else:
            self.bib_fields[entry_title] = entry_value

    def make_author_list(self, entry_value):
        name_is_last_to_first = False
        author_names = entry_value.split(" and ")
        for author_name in author_names:
            last_name = ""
            middle_name = ""
            first_name = ""
            if author_name.find(",")>=0:
            #if name_is_last_to_first:
                author_name_break = author_name.split(",")
                num_breaks = len(author_name_break)
                last_name = author_name_break[0].strip()
                first_name = author_name_break[1].strip()
            else:
                ispace = author_name.rfind(" ")
                first_name = author_name[:ispace].strip()
                last_name = author_name[ispace:].strip()
            ispace = first_name.find(" ")
            if ispace>=0:
                middle_name = first_name[ispace:].strip()
                first_name = first_name[:ispace].strip()
            if self.print_process: print(f"#################### author : {first_name}/{middle_name}/{last_name}")
            if len(self.author_list)==0:
                self.author1 = [first_name, middle_name, last_name]
            self.author_list.append([first_name, middle_name, last_name])
        self.bib_fields["author"] = self.author_list

if __name__ == "__main__":
    bib_manager("input")
    #bib_manager("")
