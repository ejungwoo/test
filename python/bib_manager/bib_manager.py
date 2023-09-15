import os

class bib_manager:

    def __init__(self, bibtex_input):
        self.print_process = False
        self.clear()
        self.journal_list = [] # should not be inside the clear method
        self.read_list_of_journals() # ???????????????
        self.read_bibtex(bibtex_input)

    def clear(self):
        self.bib_name = ""
        self.bib_entries = {}
        self.author1 = []
        self.collaboration = ""
        self.author_list = []

    def read_list_of_journals(self):
        with open('list_of_journals','r') as f1: lines = f1.readlines()
        for line in lines:
            line = line.strip()
            full_name, minimum_name, short_name = line.split('/')
            full_name, minimum_name, short_name = full_name.strip(), minimum_name.strip(), short_name.strip()
            if self.print_process: print(f"{full_name} / {minimum_name} / {short_name}")
            if len(full_name)>0:
                self.journal_list.append([full_name, minimum_name, short_name])

    def read_bibtex(self, bibtex_input):
        with open(bibtex_input,'r') as f1: lines = f1.read()
        while True:
            print()
            print()
            if self.print_process:
                print(f"=====================================================")
                print(lines)
                print(f"=====================================================")
            self.clear()
            ibr1 = lines.find("@")
            ibr2 = lines.find("{")
            icomma = lines.find(",")
            self.bib_entries["type"] = lines[ibr1+1:ibr2]
            self.bib_name = lines[ibr2+1:icomma]
            found_aa = False
            lines = lines[icomma+1:]
            while True:
                lines, entry_title, entry_value = self.find_next_entry(lines)
                entry_title = entry_title.lower()
                if entry_title=="": break
                if entry_title=="author": self.make_author_list(entry_value)
                if entry_title=="pages": self.make_pages(entry_value)
                if entry_title=="journal": self.make_journal(entry_value) 
                if entry_title=="archiveprefix": self.make_archivePrefix(entry_value) 
                if entry_title=="school": self.make_school(entry_value) 
                if entry_title=='"': continue
                if entry_title=="@":
                    found_aa = True
                    break
                if self.print_process: print(f"++++++++++++++++++++ entry : {entry_title} {entry_value}")
                self.bib_entries[entry_title] = entry_value
            self.make_bib()
            print(f' 0. name                {self.make_bib_name()}  ({self.bib_name})')
            list_of_keys = []
            for key in self.bib_entries:
                print(f"{len(list_of_keys):>2}. {key:20}{self.bib_entries[key]}")
                list_of_keys.append(key)
            if found_aa==False:
                break

    def make_bib(self):
        if self.bib_entries["type"]=="misc":
            key_contain_arxiv = ("archiveprefix" in self.bib_entries)
            url_contain_arxiv = (self.bib_entries["url"].find("arxiv.org")>=0)
            if key_contain_arxiv or url_contain_arxiv:
                self.make_journal("Arxiv")
                eprint = self.bib_entries["eprint"]
                if eprint.find("/")>=0:
                    self.bib_entries["volume"] = eprint.split("/")[0]
                    self.bib_entries["pages1"] = eprint.split("/")[1]
                elif eprint.find(".")>=0:
                    self.bib_entries["volume"] = eprint.split(".")[0]
                    self.bib_entries["pages1"] = eprint.split(".")[1]
                self.bib_entries["volume"] = self.bib_entries["volume"].replace("-","")
            else:
                self.bib_entries["journal"] = ["","",""]
                self.bib_entries["volume"] = ""
                self.bib_entries["pages1"] = ""
        if self.bib_entries["type"]=="phdthesis":
            self.bib_entries["journal"] = ["Thesis","Thesis","Thesis"]
            self.bib_entries["volume"] = ""
            self.bib_entries["pages1"] = ""

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
        count_c = 0
        prev_c = ""
        for curr_c in lines:
            count_c = count_c + 1
            if signal_end_of_value:
                if curr_c==',': break
                elif curr_c==' ' or curr_c=="\n": continue
                else:
                    break
                    count_c = count_c - 1
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

            prev_c = curr_c
            entry_value = entry_value + curr_c
        lines = lines[count_c:]
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
        colb = self.get_collaboration_name() 
        jour = self.bib_entries["journal"][1]
        year = self.bib_entries["year"]
        volm = self.bib_entries["volume"]
        page = self.bib_entries["pages1"]
        comm = ""
        if len(name)>0: name = name + "_"
        if len(colb)>0: colb = colb + "_"
        if len(jour)>0: jour = jour + "_"
        if len(year)>0: year = "y" + year + "_"
        if len(volm)>0: volm = "v" + volm + "_"
        if len(page)>0: page = "p" + page + "_"
        if len(comm)>0: comm = comm + "_"
        bib_name = name + colb + jour + year + volm + page + comm
        bib_name = bib_name[:-1]
        return bib_name

    def get_collaboration_name(self):
        return self.collaboration

    def make_nospace_author_name(self, author):
        first_name  = author[0].replace(".","").strip().title()
        middle_name = author[1].replace(".","").strip().title()
        last_name   = author[2].replace(".","").strip().title()
        return last_name+first_name+middle_name

    def make_school(self, entry_value):
        pass

    def make_archivePrefix(self, entry_value):
        self.make_journal("Arxiv")

    def make_journal(self, entry_value):
        found_etnry = False
        for journal_entry in self.journal_list:
            if journal_entry[0]==entry_value:
                self.bib_entries["journal"]=journal_entry
                found_etnry = True
                break
        if found_etnry==False:
            print(f"WARNING! Add journal {entry_value} to journal list")
            return
        if self.print_process: print(f'++++++++++++++++++++ journal : {self.bib_entries["journal"][0]}  /  {self.bib_entries["journal"][1]}  /  {self.bib_entries["journal"][2]}')

    def make_pages(self, entry_value):
        self.bib_entries["pages1"] = ""
        self.bib_entries["pages2"] = ""
        if entry_value.find("--")>=0:
            self.bib_entries["pages1"] = entry_value.split("--")[0]
            self.bib_entries["pages2"] = entry_value.split("--")[1]
        elif entry_value.find("-")>=0:
            self.bib_entries["pages1"] = entry_value.split("-")[0]
            self.bib_entries["pages2"] = entry_value.split("-")[1]
        else:
            self.bib_entries["pages1"] = entry_value
            self.bib_entries["pages2"] = 0
        if self.print_process: print(f'++++++++++++++++++++ pages : {self.bib_entries["pages1"]} - {self.bib_entries["pages2"]}')

    def make_author_list(self, entry_value):
        name_is_last_to_first = False
        if entry_value.find(",")>=0:
            name_is_last_to_first = True
        author_names = entry_value.split(" and ")
        print(author_names)
        for author_name in author_names:
            last_name = ""
            middle_name = ""
            first_name = ""
            if name_is_last_to_first:
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
            if self.print_process: print(f"++++++++++++++++++++ author : {first_name}/{middle_name}/{last_name}")
            if len(self.author_list)==0:
                self.author1 = [first_name, middle_name, last_name]
            self.author_list.append([first_name, middle_name, last_name])

if __name__ == "__main__":
    bib_manager("input")
