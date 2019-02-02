# -*- coding: utf8 -*
from toolbox import log_record

'''
модуль для чтения настроек из текстового файла "opt.txt"
'''

def parse_string(line:str):
    if line.endswith('\n'):
        line = line[0:len(line)-1]
    line_list = line.split('=')
    name_opt = line_list[0].strip(' ')
    value_opt = line_list[1].strip(' ')
    if name_opt == 'elements' \
       or name_opt == 'mainmenu' \
       or name_opt == 'sectionmenu' \
       or name_opt == 'login' \
       or name_opt == 'password' \
       or name_opt == 'mode':
        tuple_param = tuple(value_opt.split(','))
        tuple_value = tuple()
        for i in tuple_param:
            tuple_value += (i.strip(),)
        tuple_result = ((name_opt, tuple_value,),)
    else:
        tuple_result = ((name_opt, value_opt,),)
    return tuple_result


def read_opt():
    '''
    возвращает кортеж с кортежами настроек из файла "opt.txt"
    количество кортежей внутри равно количеству настроек
    в каждом кортеже два элемента:
    result_tuple[0] - имя настройки(строка)
    result_tuple[1] - значение настройки(строка или кортеж строк)
    '''
    result_tuple = tuple()
    try:
        with open("opt.txt", "r") as my_file:
            for line in my_file:
                if line[0] == '#':
                    continue
                elif len(line) < 3:
                    continue
                elif line.find('=') == -1:
                    continue
                else:
                    result_tuple += parse_string(line)
    except:
        log_record('программа не нашла файл opt.txt')
    my_file.close()
    return result_tuple


