import string

class file:

    def __init__(self, address, name=False, version = False, author=False, date=False):
        """Initialization of an object: address of file
            - takes an file address and check if ot is a python (.py) program
            - downloads file as list of lines, saves it under 'content' name
            - saves list of external packages as 'externals'
            - saves author and date of program
            - aggregates spaces in file in an default way
        """

        # saving input data
        self.__name = name
        self.__author = author
        self.__date   = date
        self.__version = version

        #checking py
        self.__gooodAddressFlag = self.__init_check_py(address)

        if self.__gooodAddressFlag:

            self.__init_download_content(address)
            self.__init_find_externals()



    # axuliary init functions

    def __init_check_py(self, address):
        "Checks if last part if name is '.py'"

        try:

            if address.split('.')[-1] == 'py':
                return True
            else:
                return False

        except:

            return False


    def __init_download_content(self, address):
        "Downloads file content and saves as '__content'"

        #creation of empty list of content
        self.__content = []

        with open(address, 'r') as file:
            self.__content = file.readlines()


    def __init_find_externals(self):
        "Searches external inputs."

        self.__externals = []

        for x in self.__content:

            # Removing empty spaces
            line = self.__comm_remov_f_empt(x)

            # Checking lines
            line_splitted = line.split(' ')

            if line_splitted[0] in ['import', 'from']:

                self.__externals.append(line_splitted[1])

    # aggregators

    def __default_aggregation(self):
        "Aggregates content in default manner"

        # final lines of code
        tab_lines = []

        # adding top lines
        top_lines = self.__aggr_top()
        for x in top_lines: tab_lines.append(x)


        pass

    # axuliary aggregate functions

    def __aggr_top(self, top_tab):
        "Organizes nice looking top"

        # init output list
        ready_top_tab = []

        # function that gives proper item
        dict_items={
                    'name':   self.__name,
                    'version':self.__version,
                    'author': self.__author,
                    'date':   self.__date}

        # iterating lines and replacing symbols with data
        for line in top_tab:

            # saving proper line
            ready_top_tab += self.__comm_replace_item_line(line, dict_items)

        # ready output
        return ready_top_tab


    def __aggr_externals_constants(self, exter_list, const_list):
        "Finds external links on the top and organizes nice looking paragraph"
        
        # table for upper lines
        upper_lines = []

        for x in self.__content:

            if self.__comm_remov_f_empt(x).split(' ')[0] in ["def", "class"]: break
            upper_lines.append(x)
        
        upper_lines=upper_lines[:-1]

        # picking external links
        external_lines = []
        end_externals_line = 0

        for i in range(len(upper_lines)):

            if self.__comm_remov_f_empt(upper_lines[i]).split(' ')[0] in ["from", "import"]:

                external_lines.append(upper_lines[i])
                end_externals_line=i

        # saving raw table with constants
        constant_lines = upper_lines[end_externals_line:]

        new_paragraph_flag = False
        for x in external_lines:
            .


    def __agg_paragraph_maker(self, list, space):
        "Aggregates properly paragraph."

        # init buffer and output list
        buff_0_list = []
        buff_1_list = []
        out_list = []

        # first iteration - proper empty lines spaces
        for x in list:

            empty_line = True
            empty_lin_chkd = False

            for n in x:

                if n in list(string.ascii_lowercase): empty_line = False

            if   empty_line and empty_lin_chkd: pass
            elif empty_line:
                empty_lin_chkd = True
                for i in range(space): buff_0_list.append('')
            else: buff_0_list.append(x)
        
        # second iteration - space edition
        flag_empty_sp_not = True

        for i in range(len(buff_0_list)):

            if flag_empty_sp_not:

                if buff_0_list[i] == '' and (i+3)<len(buff_0_list):

                    if self.__comm_remov_f_empt(buff_0_list[i+3])[0] == '#':

                        for j in range(3): buff_1_list.append('')
                        flag_empty_sp_not = False

            if self.__comm_remov_f_empt(buff_0_list[i+3])[0] == '#' and i-1>=0:

                if buff_0_list[i-1] != '':

                    for j in range(3): buff_1_list.append('')
                    buff_1_list.append(buff_0_list[i])
                    flag_empty_sp_not = True

            elif buff_0_list[i] != '':

                buff_1_list.append(buff_0_list[i])
                flag_empty_sp_not = True

        # loop spaces and comments
        loop_strd_flag = [False, False]

        for i in range(len(buff_1_list)):

            if self.__comm_remov_f_empt(buff_1_list[i])[0] in ['if', 'elif', 'else', 'while']:

                temp=[]

                n = self.__comm_count_frnt_spc(buff_1_list[i])
                loop_strd_flag = [True, n]

                if i-2>=0:

                    if buff_1_list[i-2]!='':

                        for j in range(space[0]): temp.append('')

                if i-1>=0:

                    if self.__comm_remov_f_empt(buff_1_list[i-1])[0]=='#' and self.__comm_count_frnt_spc(buff_1_list[i-1])==n:

                        pass

                    else:

                        comment = ''
                        for j in range(n): comment+=' '
                        temp.append(comment + '#loop')
                
                temp.append(buff_1_list[i])

                if i+1<len(buff_1_list):

                    if buff_1_list[i+1] != '':

                        for j in range(space[1]): temp.append('')
            
                for x in temp: out_list.append(x)

            elif loop_strd_flag[0] and self.__comm_count_frnt_spc(buff_1_list[i])==loop_strd_flag[1]:

                for j in range(space[2]): out_list.append('')
                out_list.append(buff_1_list[i])
                loop_strd_flag = [False, False]
            
            else: out_list.append(buff_1_list[i])






    # universal formating function

    def __form_univers(self, lines, base_type):
        """ Takes line list and creates frper format.
              - base_type = 'class' - 'class' is main paragraph, functions are lower, variables are treated like a text.
              - base_type = 'def'   - function is  main paragraph, lower functions are lower, variables are treated like a text.
              - base_type = 'var'   - there is top and bottom comment for variables and equations"""
        .









    # axuliary common functions

    def __comm_remov_f_empt(self, str_line):
        "Removing first empty line"

        line = ''
        first_empty = True

        for n in str_line:

            if first_empty and n != ' ':    first_empty = False

            else:

                line+=n

        return line


    def __comm_replace_item_line(self, line, possibles_dict=False):
        "Replaces %item% elements in line"

        # variables to edit top template
        buff = ''
        item_name = ''
        place_flag = False

        # reprint line with given data (items)
        for n in line:

            if   place_flag == False and n!='%': buff+=n
            elif place_flag == False and n=='%': place_flag = True
            elif place_flag and n!='%': item_name+=n
            elif place_flag and n=='%':
                buff += possibles_dict[item_name]
                item_name = ''
                place_flag = False

        return buff


    def __comm_count_frnt_spc(self, line):
        "Counts empty spaces in front of line."

        count = 0

        for x in line:

            if x==' ': count+=1
            else: return count
