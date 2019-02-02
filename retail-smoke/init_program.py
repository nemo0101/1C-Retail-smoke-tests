# -*- coding: utf8 -*
from time import sleep

from main_data import MainData
from toolbox import exit_prog, log_record
from read_options import read_opt
from webdriver import (
    get_webdriver,
    open_url,
    wait_window,
    get_webdriver_quit,
    find_one_element_by_id,
    get_info_from_element
    )
from keyboard_and_mouse_tools import (
    get_foreground_window,
    full_screen,
    push_button_on_keyboard,
    return_wscript_shell,
    simple_click,
    simple_enter_text,
    get_window_rect,
    search_hwnd)


'''
модуль для запуска браузера и входа в 1с
'''

def init_prog(tuple_main_data:tuple):
    '''
    получает пустой кортеж,
    получает вебдрайвер, wscript_shell и настройки из opt.txt
    инициализирует объект main_data который будет хранить другие объекты, таблицы и настройки
    проходя через все функции
    '''
    tuple_main_data += (get_webdriver(),)
    tuple_main_data += (return_wscript_shell(),)
    tuple_main_data += (read_opt(),)
    main_data = MainData(tuple_main_data)
    return main_data


def start_browser(main_data:object):
    open_url(
        main_data.driver(),
        main_data.base_url()
    )
    hwnd = get_foreground_window()
    full_screen(hwnd)
    win_rect = get_window_rect(hwnd)
    if wait_window(
        main_data.driver(),
        main_data.auth_win(),
        1000):
            main_data.set_hwnd(hwnd)
            main_data.set_win_rect(win_rect)
            return main_data
    else:
        get_webdriver_quit(main_data.driver())
        exit_prog()


def login_base(main_data:object):
    '''
    выполняет вход в базу: вводит логин, пароль, нажимает кнопку "ok"
    ждет когда загрузится программа, ждет и пытается закрыть окно поддержки 1с
    '''
    login_elem = get_info_from_element(
                    find_one_element_by_id(
                            main_data.driver(),
                            main_data.login_opt()[0]
        )
    )
    password_elem = get_info_from_element(
                        find_one_element_by_id(
                                main_data.driver(),
                                main_data.passw_opt()[0]
        )
    )
    ok_elem = get_info_from_element(
                find_one_element_by_id(
                        main_data.driver(),
                        main_data.ok_button_opt()
        )
    )
    simple_enter_text(
        main_data,
        login_elem,
        main_data.login_opt()[1]
    )
    simple_enter_text(
        main_data,
        password_elem,
        main_data.passw_opt()[1]
    )
    simple_click(main_data, ok_elem)

    if wait_window(
        main_data.driver(),
        main_data.mainmenu()[0],
        1000
        ) == True:
            if wait_window(main_data.driver(), 'ps0formHeaderTitle', 10) == True:
                push_button_on_keyboard(
                    main_data.hwnd(), 
                    main_data.wscript_shell(), 
                    'esc', 
                    1
                )
            log_record('выполнен вход в базу')
            return main_data
    else:
        get_webdriver_quit(main_data.driver())
        exit_prog()


def reload(main_data:object):
    if search_hwnd(main_data.hwnd()) == False:
        '''
        table = main_data.table_elements()
        main_data = login_base(
            start_browser(
                init_prog(tuple())
            )
        )
        main_data.set_table_elements(table)
        log_record('выполнен перезапуск')
        '''
        exit_prog()

