# -*- coding: utf8 -*
from init_program import (
    init_prog, 
    start_browser,
    login_base
)
from full_cycle import menu_full_cycle_go, page_full_cycle_go
from serializer import write_serialize_data, read_serialize_data
from toolbox import log_record, exit_prog
from keyboard_and_mouse_tools import push_button_on_keyboard
from scenario_mod import start_scenario
from cursor_pos import cursor_pos
from partial_cycle import start_partial_cycle
from go_open_form import open_forms
from webdriver import get_webdriver_quit


def check_table_elements(main_data:object):
    table_elements = main_data.table_elements()
    if len(table_elements['table']) == 0 or table_elements == None:
        get_webdriver_quit(main_data.driver())
        log_record('программа прекратила работу, нет сохраненной таблицы меню, воспользуйтесь созданием данной таблицы через запуск программы в режиме savemenu')
        exit_prog()


def main_func():
    log_record('НАЧАЛО РАБОТЫ ПРОГРАММЫ')
    main_data = login_base(
        start_browser(
            init_prog(tuple())
        )
    )
    for m in main_data.mode():
        if m == 'savemenu':
            log_record('началось чтение разделов меню программы')
            main_data = menu_full_cycle_go(main_data)
            write_serialize_data('dict_main_elements', main_data.table_elements())
            get_webdriver_quit(main_data.driver())
            log_record('завершено чтение разделов меню программы, разделы сохранены в файл dict_main_elements.pickle')
        elif m == 'go':
            log_record('начался обход')
            main_data.set_table_elements(
                read_serialize_data(text='dict_main_elements', remove_arg=False)
            )
            check_table_elements(main_data)
            page_full_cycle_go(main_data)
            get_webdriver_quit(main_data.driver())
            log_record('обход завершен')
        elif m == 'scenario':
            start_scenario(main_data)
            get_webdriver_quit(main_data.driver())
            log_record('закончено выполнение сценария')
        elif m == 'cursor':
            cursor_pos(main_data)
        elif m == 'go_partial':
            log_record('начался частичный обход')
            main_data.set_table_elements(
                read_serialize_data(text='dict_main_elements', remove_arg=False)
            )
            check_table_elements(main_data)
            start_partial_cycle(main_data)
            get_webdriver_quit(main_data.driver())
            log_record('частичный обход завершен')
        elif m == 'open_forms':
            log_record('начался обход открытия форм')
            main_data.set_table_elements(
                read_serialize_data(text='dict_main_elements', remove_arg=False)
            )
            check_table_elements(main_data)
            open_forms(main_data)
            get_webdriver_quit(main_data.driver())
            log_record('закончился обход открытия форм')


if __name__ == "__main__":
    main_func()
