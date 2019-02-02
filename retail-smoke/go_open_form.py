# -*- coding: utf8 -*
from full_cycle import click_or_enter_text, wait_win_1c_head, wait_msg, push
from keyboard_and_mouse_tools import push_button_on_keyboard
from parse_webelements import parse_elements_on_page
from webdriver import get_page


def click_main_and_section(main_elem, section_elem, main_data):
    click_or_enter_text(main_elem, main_data)
    click_or_enter_text(section_elem, main_data)


def open_forms(main_data:object):
    table = main_data.table_elements()['table']
    for x in table:
        for y in x['table']['table']:
            #if x['text_elem'] == 'Продажи':
            if y['id_elem'] != 'cmd_2_7': # РМК
                click_main_and_section(x, y, main_data)
                push('insert', 1, main_data)
                push('esc', 4, main_data)

