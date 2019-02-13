# -*- coding: utf8 -*
from toolbox import cons_input, parse_data_input, log_record, exit_prog, print_string
from full_cycle import start, get_page_info
from webdriver import get_webdriver_quit


'''
обход из заданного в консоли места (mode=go_partial)
'''


def filter_for_main_elements(element:str, data:tuple):
    main_elem = None
    for x in data:
        if x['text_elem'] == element:
            main_elem = x
            break
    return main_elem


def chek_input_element(input_element, main_data):
    if input_element == None:
        get_webdriver_quit(main_data.driver())
        log_record('ошибка ввода названия раздела меню в консоль')
        print_string('ошибка ввода')
        exit_prog()


def start_partial_cycle(main_data:object):
    cons_input_res = parse_data_input(
                        cons_input()
    )
    if len(cons_input_res) == 2:
        main_elem = filter_for_main_elements(cons_input_res[0], main_data.table_elements()['table'])
        chek_input_element(main_elem, main_data)
        section_elem = filter_for_main_elements(cons_input_res[1], main_elem['table']['table'])
        chek_input_element(section_elem, main_data)
        main_data.set_table_elements(
            (
                get_page_info(main_data, main_elem, section_elem), 
            )
        )
        start(main_data)
