# -*- coding: utf8 -*
from full_cycle import click_or_enter_text, push


'''
основная логика работы для режима open_form
'''


def click_main_and_section(main_elem, section_elem, main_data):
    click_or_enter_text(main_elem, main_data)
    click_or_enter_text(section_elem, main_data)


def open_forms(main_data:object):
    table = main_data.table_elements()['table']
    for x in table:
        for y in x['table']['table']:
            click_main_and_section(x, y, main_data)
            push('insert', 1, main_data)
            push('esc', 4, main_data)

