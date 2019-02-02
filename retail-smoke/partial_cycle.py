# -*- coding: utf8 -*
from toolbox import cons_input, parse_data_input, log_record, exit_prog, print_string
from full_cycle import click_or_enter_text, cycle, get_current_page
from webdriver import get_webdriver_quit

'''
обход из заданного в консоли места (mode=go_partial)
'''


def filter_for_main_elements(element:str, data:tuple):
    main_elem = None
    for x in data:
        if x['text_elem'] == element:
            x['click'] = True
            main_elem = x
            break
    return main_elem


def go_partyal_cycle(main_data:object, main_elem:dict, section_elem:dict):
    page_opt = (main_data.page(), main_data.elements(),)
    if main_elem != None:
        main_elem['click'] = True
        click_or_enter_text(main_elem, main_data)
        if section_elem != None:
            section_elem['click'] = True
            click_or_enter_text(section_elem, main_data)
            section_elem['table'] = get_current_page(main_data.driver(), page_opt)
            if len(section_elem['table']['table']) > 0:
                section_table = {'table':(section_elem, ), 'len_table':0, 'number_of_pages':0, 'context_tables':tuple()}
                main_elem['table'] = section_table
                main_table = {'table':(main_elem, ), 'len_table':0, 'number_of_pages':0, 'context_tables':tuple()}
                main_data.set_table_elements(main_table)

                table = cycle(section_table['table'][0]['table'], main_data)

        else:
            log_record('не найден элемент меню разделов')
    else:
        log_record('не найден элемент главного меню')


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
        go_partyal_cycle(main_data, main_elem, section_elem)
