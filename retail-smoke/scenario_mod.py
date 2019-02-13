# -*- coding: utf8 -*
from os import path, curdir
from time import sleep

from toolbox import (
    cons_input, 
    try_except_log_ret, 
    log_record, 
    copy_to_clipboard,
    parse_data_input
)
from serializer import get_filenames_in_curdir
from keyboard_and_mouse_tools import (
    click, 
    push_button_on_keyboard, 
    set_foreground_window,
    set_window_pos
)


'''
отвечает за воспроизведение сценариев (mode=scenario)
'''


def search_comment(line:str):
    if line.find('#') == -1:
        line_list = [line,]
    else:
        line_list = line.split('#')
    line_list = line_list[0].split(',')
    line_list = [i.strip() for i in line_list]
    return line_list


def parse_str_in_file(line:str):
    list_line = line.split('=')
    if len(list_line) == 2:
        return (
            {
                search_comment(list_line[0])[0]:
                search_comment(list_line[1])
             },
        )
    else:
        log_record('в сценарии больше чем один знак: =')


def start_read_file(res:tuple):
    tuple_commands = tuple()
    try:
        with open(res[0], "r") as my_file:
            for line in my_file:
                if line[0] == '#':
                    continue
                elif line.find('=') == -1:
                    continue
                else:
                    tuple_commands = tuple_commands + parse_str_in_file(line)
    except:
        log_record('не удалось открыть файл')
    return tuple_commands


def parse_file_scenario(data_list:tuple):
    tuple_commands = tuple()
    current_dir = try_except_log_ret(path.abspath, curdir)
    for x in data_list:
        res = get_filenames_in_curdir(x, current_dir)
        if len(res) == 1:
            tuple_commands = tuple_commands + start_read_file(res)
        else:
            log_record('файл ' + x + ' отсутствует, либо по данному наименованию присутствует больше чем один файл')
    return tuple_commands


def key_func_list_scenario(param_list:list):
    tuple_commands = parse_file_scenario(tuple(param_list))
    for command in tuple_commands:
        exec_command(command)


def key_func_win(param_list):
    if len(param_list) == 4:
        param_list = [int(x) for x in param_list]
        res = param_list
    else:
        log_record('координаты верхнего угла приложения отличны от четырех параметров')
        res = None
    return res


def key_func_click(value, main_data):
    if len(value) == 2:
        value = [int(x) for x in value]
        set_foreground_window(main_data.hwnd())
        click(value[0], value[1])
        sleep(1)
    else:
        log_record('неправильно заданы координаты')


def key_func_duble_click(value, main_data):
    if len(value) == 2:
        value = [int(x) for x in value]
        set_foreground_window(main_data.hwnd())
        click(value[0], value[1])
        sleep(1)
        click(value[0], value[1])
        sleep(1)
    else:
        log_record('неправильно зада    ны координаты')


def key_func_input(value, main_data):
    for x in value:
        copy_to_clipboard(x)
        push_button_on_keyboard(main_data.hwnd(), main_data.wscript_shell(), 'paste')
        log_record('введен текст: '+ x)
        sleep(1)


def key_func_press_button(value, main_data):
    for x in value:
        push_button_on_keyboard(main_data.hwnd(), main_data.wscript_shell(), x)
        sleep(1)


def key_func_sleep(value):
    for x in value:
        sleep(int(x))


def exec_command(comm:dict, main_data:object):
    key = comm.keys()
    value = comm.values()
    if len(key)!=0 and len(value)!=0:
        key = list(key)[0]
        value = list(value)[0]
        res = None
        if key == 'lst':
            key_func_list_scenario(value)
        elif key == 'win':
            res = key_func_win(value)
        elif key == 'cl':
            key_func_click(value, main_data)
        elif key == 'd_cl':
            key_func_duble_click(value, main_data)
        elif key == 'in':
            key_func_input(value, main_data)
        elif key == 'pr':
            key_func_press_button(value, main_data)
        elif key == 'sl':
            key_func_sleep(value)
        return res


def start_scenario(main_data:object):
    tuple_commands = parse_file_scenario(
                        parse_data_input(
                            cons_input()
                        )
    )
    set_foreground_window(main_data.hwnd())
    win_coord = exec_command(tuple_commands[0], main_data)
    if len(tuple_commands) != 0 and \
        len(win_coord) == 4:
            width = win_coord[0] + win_coord[2]
            height = win_coord[1] + win_coord[3]
            set_window_pos(main_data.hwnd(), win_coord[0], win_coord[1], width, height)
            for command in tuple_commands:
                exec_command(command, main_data)
    else:
        log_record('первая строчка в сценарии не кординаты окна')