# -*- coding: utf8 -*
import logging
from init_program import (
    init_prog, 
    start_browser,
    login_base
)
from full_cycle import menu_full_cycle_go, page_full_cycle_go
from serializer import write_serialize_data, read_serialize_data, delete_screens_and_log
from toolbox import log_record, exit_prog
from scenario_mod import start_scenario
from cursor_pos import cursor_pos
from partial_cycle import start_partial_cycle
from go_open_form import open_forms
from webdriver import get_webdriver_quit


'''
главный модуль программы
запуск программы происходит из этого модуля
'''


def check_table_elements(main_data:object):
    table_elements = main_data.table_elements()
    if table_elements == None or len(table_elements['table']) == 0:
        get_webdriver_quit(main_data.driver())
        log_record('программа прекратила работу, нет сохраненной таблицы меню, воспользуйтесь созданием данной таблицы через запуск программы в режиме savemenu')
        exit_prog()


def check_end(main_data, last_mode:str, curr_mode:str, str_log:str):
    if last_mode == curr_mode:
        get_webdriver_quit(main_data.driver())
        log_record(str_log)
        logging.shutdown()


def main_func():
    main_data = login_base(
        start_browser(
            init_prog(tuple())
        )
    )
    mode = main_data.mode()
    last_mode = mode[-1]

    if main_data.del_screen_and_log() == 'Yes':
        delete_screens_and_log()

    log_record('НАЧАЛО РАБОТЫ ПРОГРАММЫ')
    for m in mode:
        if m == 'savemenu':
            log_record('началось чтение разделов меню программы')
            old_table = read_serialize_data('dict_main_elements')
            del old_table
            main_data = menu_full_cycle_go(main_data)
            write_serialize_data('dict_main_elements', main_data.table_elements())
            check_end(main_data, last_mode, 'savemenu', 'разделы сохранены в файл dict_main_elements.pickle')
        elif m == 'go':
            log_record('начался обход')
            main_data.set_table_elements(
                read_serialize_data(text='dict_main_elements', remove_arg=False)
            )
            check_table_elements(main_data)
            page_full_cycle_go(main_data)
            check_end(main_data, last_mode, 'go', 'обход завершен')
        elif m == 'scenario':
            start_scenario(main_data)
            check_end(main_data, last_mode, 'scenario', 'закончено выполнение сценария')
        elif m == 'cursor':
            cursor_pos(main_data)
        elif m == 'go_partial':
            log_record('начался частичный обход')
            main_data.set_table_elements(
                read_serialize_data(text='dict_main_elements', remove_arg=False)
            )
            check_table_elements(main_data)
            start_partial_cycle(main_data)
            check_end(main_data, last_mode, 'go_partial', 'частичный обход завершен')
        elif m == 'open_forms':
            log_record('начался обход открытия форм')
            main_data.set_table_elements(
                read_serialize_data(text='dict_main_elements', remove_arg=False)
            )
            check_table_elements(main_data)
            open_forms(main_data)
            check_end(main_data, last_mode, 'open_forms', 'закончился обход открытия форм')


if __name__ == "__main__":
    main_func()
