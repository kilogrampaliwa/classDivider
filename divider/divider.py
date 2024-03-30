
class divide:

    def __init__(self, address: str, spaces=False):
        "Takes address and creates lists for classes and functions."

        # template
        template = {
            "externals" : [],
            "upName"    : False,
            "content"   : []
        }

        # checks spaces
        self.spaces = spaces
        if spaces:
            if isinstance(spaces, bool): self.spaces = 1
        else: spaces = 0

        # raw data
        self.__raw_lines = self.__download_file(address)
        isClasses = self.__find_if_classes(self.__raw_lines)

        # main lists
        self.__classes = []
        self.__functions = []

        # check and create classes
        if isClasses[0]:

            for x in isClasses[1]:

                buff_dict = template.copy()
                buff_dict["externals"] = self.__save_externals(self.__raw_lines)
                buff_dict["upName"] = address
                buff_dict["content"] = x
                self.__classes.append(buff_dict)

        else: self.__classes = False

        # check and create functions
        if isClasses[0]:

            for x in self.__classes:

                names = self.__find_name(x["content"][0])

                for y in self.__divide_functions(x["content"]):

                    buff_dict = template.copy()
                    buff_dict["externals"] = x["externals"]
                    buff_dict["upName"] = names
                    buff_dict["content"] = self.__clean_function_list(y, names, buff_dict["externals"]) #y
                    self.__functions.append(buff_dict)


    def save(self):
        "Saving to seprate files."
        for x in self.__functions: self.__save_file(x['content'])


    def __save_file(self, lines: list[str]):
        "Saves lines as a .py file."
        with open(self.__find_name(lines[1], 'def')+'.py', 'w') as file:
            file.writelines(lines)


    def __find_name(self, first_line, type='class'):
        "Takes name from first line."

        name = ''
        if first_line[0]==' ': first_line = self.__delete_empty_first(first_line)
        if   type=='def':   first_line = self.__delete_empty_first(first_line[4:])
        elif type=='class': first_line = self.__delete_empty_first(first_line[5:])
        flag_no_bracket = True

        i = 0
        while flag_no_bracket:

            if first_line[i] in ['(', ':']: flag_no_bracket = False
            else: name+=first_line[i]
            i+=1

        name = name.split(' ')[-1]

        return name


    def __find_def_class(self, lines: list[str], type='def'):
        "Finding place of 'def' or 'class'."

        # place list
        place_list = []

        # searching 'def's or 'class'es
        for i in range(len(lines)):

            line_empt = self.__delete_empty_first(lines[i])
            buff_6 = [False, False, False, False, False, False]

            for x in line_empt:

                buff_6 = buff_6[1:]
                buff_6.append(x)

                if   type=='def'   and (buff_6[:4]== ['d','e','f',' '] or buff_6[:4]== 'def '):
                    place_list.append(i)
                    break
                elif type=='class' and (buff_6== ['c','l','a','s','s',' '] or buff_6== 'class '):
                    place_list.append(i)
                    break

        # return found places
        if place_list==[]: return False
        else:              return place_list


    def __download_file(self, address: str):
        "Downloading .py file"

        # lines of file
        self.__lines = False

        # table of lines in file
        lines = []

        # load from file
        with open(address, 'r') as file:    return file.readlines()


    def __divide_functions(self, line_list: list[str]):
        "Picking functions to different tables."

        # place list
        place_list = []

        # listo of lists to be ready
        ready_lists = []

        # searching 'def's
        place_list = self.__find_def_class(line_list, 'def')
        
        # remember spaces
        spaces = []
        for x in place_list:    spaces.append(self.__count_front_space_def(line_list[x]))

        # division
        for i in range(len(place_list)-1):

            buff_list = line_list[place_list[i]:place_list[i+1]]
            ready_lists.append(buff_list)

        ready_lists.append(line_list[place_list[-1]:])

        # remoce spaces
        for i in range(len(ready_lists)):

            buff_def = []

            for m in ready_lists[i]:
                m = m[spaces[i]:]
                buff_def.append(m)

            ready_lists[i] = buff_def

        # output
        return ready_lists


    def __count_front_space_def(self, line: str):
        "Counts empty spaces before function declaration."

        # out count
        count = 0

        # loop
        space_flag = True
        while space_flag:
            if line[count] == ' ': count+=1
            else: space_flag = False
        
        # returning count
        return count


    def __find_if_classes(self, lines: list[str]):
        "Find if classes and returns lists of different classes."

        # exist
        class_flag = False

        # listo of lists to be ready
        ready_lists = []

        # place lists
        start_place_list = []
        stop__place_list = []

        # search
        found_classes = self.__find_def_class(lines, 'class')

        if found_classes:
            start_place_list = found_classes
            class_flag = True

        # division
        if class_flag:

            # creating stops
            if len(start_place_list)>=2:
                for x in start_place_list[1:]: stop__place_list.append(x)
            stop__place_list.append(len(lines))

            # division
            for i in range(len(start_place_list)):
                ready_lists.append(lines[start_place_list[i]:stop__place_list[i]])

            # return if found
            return [True, ready_lists]

        # return if not found
        return [False, False]


    def __clean_function_list(self, lines: list[str], className: str, externals: list[str]):
        "Cleans list from '(self's, adding comment and globals"

        # list for output
        out_list  = []
        buff_list = []
        buff_2_list = []

        # for 'self' variables
        slf_vars = []

        # for 'self' functions
        slf_func = []

        # adding comment
        buff_list.append("#Function from class "+className + "\n")

        # finding line of declaration
        out_declaration=''
        line_of_dec = self.__find_def_class(lines, 'def')
        if line_of_dec:

            line_of_dec = line_of_dec[0]
            buff = [False, False, False, False, False, False]

            place_list = 0

            for i in range(len(lines[line_of_dec])):

                buff = buff[1:]
                buff.append(lines[line_of_dec][i])

                if buff== ['(','s','e','l','f',')'] or buff=='(self)':
                    place_list = i
                    out_declaration = lines[line_of_dec][:(place_list-5)] + '():' + '\n'
                    break
                elif buff== ['(','s','e','l','f',','] or buff=='(self,':
                    place_list = i
                    out_declaration = lines[line_of_dec][:(place_list-5)] + '(' + lines[line_of_dec][i+1:] + '\n'
                    break

        buff_list.append(out_declaration)

        # reprint lines
        for x in lines[1:]: buff_list.append(x)

        # pick all 'self's
        buff_2_list, slf_vars, slf_func = self.__slf_fuc_top(buff_list.copy())

        # create additional paragraphs
        preface = ["# 'self' variables needed to use this function:\n"]
        for x in slf_vars:
            line = "self_" + x + " = False  # common value for 'class', to be changed.\n"
            preface.append(line)
        preface.append('\n')
        preface.append("# 'self' functions needed to use this function:\n")

        for x in slf_func:
            line = 'from '+x.split('(')[0]+ ' import '+x.split('(')[0]+' as self_' + x.split('(')[0] + "    # - common function for 'class', to be changed.\n"
            preface.append(line)
        preface.append('\n\n')

        out_list.append('# Function from:  ' + className + '\n')
        out_list.append('# name - ' + buff_2_list[1] + '\n')

        if externals!=[]:
            out_list.append('\n')
            out_list.append("# External elements:\n")
            for x in externals:  out_list.append(x)
            out_list.append('\n\n')

        for x in preface:
            out_list.append(x)

        for x in buff_2_list:
            for n in range(self.spaces): out_list.append('\n')
            out_list.append(x)

        # return output
        return out_list


    def __delete_empty_first(self, line: str):
        "Deleting empty spaces at front."

        if line in ['', None]: return line
        else:

            for i in range(len(line)):

                if line[i] != ' ': return line[i:]


    def __slf_fuc_top(self, lines: list[str]):
        "Takes 'self' elements and brngs it to the top."

        # foud 'self' elements
        variables = []
        functions = []

        # loop thru all lines
        for i in range(len(lines)):

            flag_slf = False
            flag_func_brack = False
            buff = [False, False, False, False, False]
            temp_var = ''
            temp_func = ''
            brac_inside = 0
            slf_points = []
            temp_l = lines[i]

            for j in range(len(lines[i])):

                if flag_slf:
                    if lines[i][j]=='(' and flag_func_brack==False:
                        temp_func = temp_var + lines[i][j]
                        temp_var = ''
                        flag_func_brack = True
                    elif lines[i][j]=='(' and flag_func_brack:
                        brac_inside+=1
                        temp_func+=lines[i][j]
                    elif lines[i][j]==')' and brac_inside==0 and flag_func_brack:
                        brac_inside=0
                        temp_func+=lines[i][j]
                        functions.append(temp_func)
                        flag_func_brack = False
                        flag_slf = False
                    elif lines[i][j]==')' and flag_func_brack:
                        brac_inside-=1
                        temp_func+=lines[i][j]
                    elif flag_func_brack:
                        temp_func+=lines[i][j]
                    elif flag_func_brack==False and lines[i][j] in [' ', '\n', '=', '+', '/', '*', '-', ')', '}', ':']:
                        variables.append(temp_var)
                        flag_slf = False
                    else:
                        temp_var+=lines[i][j]
                else:
                    buff = buff[1:]
                    buff.append(lines[i][j])
                    if buff=='self.' or buff==['s','e','l','f','.']:
                        flag_slf = True
                        slf_points.append(j)
            if slf_points!=[]:
                for x in slf_points: temp_l = temp_l[:x-4] + 'self_' + temp_l[x+1:]
                lines[i] = temp_l


        return lines, variables, functions


    def __save_externals(self, lines: list[str]):
        "Takes all 'import's and 'from's"

        externals = []

        for x in lines:
            if x.split(' ')[0] in ['import', 'from']: externals.append(x)

        return externals



runIt = divide("x_testing_defs/divider/file_template.py")
runIt.save()