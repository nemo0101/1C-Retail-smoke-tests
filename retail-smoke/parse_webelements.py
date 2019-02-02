# -*- coding: utf8 -*
from webdriver import get_info_from_element

'''
здесь находятся функции связанные с парсингом элементов
'''


def select_elements_by_rect(element:dict):
    flag = False
    if element['rect_elem']['y'] != 0:
        flag = True
    return flag


def select_elements_by_text(element:dict):
    flag = False
    if element['text_elem'] != '':
        flag = True
    return flag


def parse_elements_by_text(elements:tuple):
    table = tuple()
    for x in elements:
        dict_element = get_info_from_element(x, 'filter_for_main_menu')
        if dict_element != None:
            if select_elements_by_text(dict_element) == True:
                table += (dict_element,)
    return table


def search_in_dict_tuple(text:str, dict_tuple:tuple):
    for dict_elem in dict_tuple:
        if dict_elem['text_elem'] == text:
            return dict_elem


def fix_text_matches(table:tuple):
    work_list = []
    work_list_append = work_list.append
    for dict_element in table:
        work_list_append(dict_element['text_elem'])
    work_list = list(set(work_list))
    result_list = []
    result_list_append = result_list.append
    for text_elem in work_list:
        result_list_append(
            search_in_dict_tuple(text_elem, table)
        )
    return tuple(result_list)


def devide_by_presence_text(table:tuple, dict_element:dict):
    if len(table) == 2:
        table_with_text = table[0]
        table_without_text = table[1]
        if dict_element['text_elem'] == '':
            table_without_text = table_without_text + (dict_element,)
        else:
            table_with_text += (dict_element,)
        table = (table_with_text, table_without_text,)
    return table


def parse_elements_on_page(elements:tuple):
    '''
    возвращаемый кортеж состоит из трех элементов:
    (кортеж словарей элементов,
    первоначальное количество элементов,
    количество первоначальных элементов предыдущей страницы)
    '''
    table = (tuple(), tuple(),)
    for x in elements:
        dict_element = get_info_from_element(x)
        if dict_element != None:
            table = devide_by_presence_text(table, dict_element)
    table_with_text = table[0]
    table_without_text = table[1]
    table_with_text = fix_text_matches(table_with_text)
    final_table = table_with_text + table_without_text
    return final_table


def sort_table(table_tuple:tuple):
    table = list(table_tuple)
    table.sort(key=lambda val: val['node_name'] == 'A')
    table.sort(key=lambda val: val['node_name'] == 'BUTTON')
    table.sort(key=lambda val: val['node_name'] == 'INPUT', reverse=True)
    return tuple(table)


def rec_search_last_open_table(bypass_table:tuple, key, click_map = []):
    if len(bypass_table['table']) != 0 and bypass_table['table'][0]['key_table'] != key:
        bypass_table = list(bypass_table['table'])
        bypass_table.reverse()
        click_map_append = click_map.append
        for dict_element in bypass_table:
            '''
            находит последнего нажатого с заполненной таблицей
            '''
            if dict_element['click'] == True and len(dict_element['table']['table']) != 0:
                click_map_append(dict_element)
                rec_search_last_open_table(dict_element['table'], key, click_map)
                break
    return tuple(click_map)