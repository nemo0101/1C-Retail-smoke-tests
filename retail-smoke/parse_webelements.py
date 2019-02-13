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
        dict_element = get_info_from_element(x)
        if dict_element != None:
            if select_elements_by_text(dict_element) == True:
                table += (dict_element,)
    return table


def search_in_dict_tuple(text:str, dict_tuple:tuple):
    for dict_elem in dict_tuple:
        if dict_elem['text_elem'] == text:
            return dict_elem


def part_id(str_test):
    len_str_test = len(str_test)
    if len_str_test > 2:
        part_str_test = round(len(str_test)*66/100)
        res_str = str_test[0:part_str_test]
    else:
        res_str = str_test
    return res_str


def fix_text_matches(table:tuple, str_mode = ''):
    work_list = []
    work_list_append = work_list.append

    for index, value in enumerate(table):
        if str_mode == 'page':
            if index == 0:
                work_list_append(value['text_elem'])
            else:
                if part_id(value['id_elem']) in table[index-1]['id_elem']:
                    continue
                work_list_append(value['text_elem'])
        else:
            work_list_append(value['text_elem'])

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
    final_table = fix_text_matches(table[0], 'page') + table[1]
    return final_table


def sort_table(table_tuple:tuple):
    table = list(table_tuple)
    table.sort(key=lambda val: val['node_name'] == 'A')
    table.sort(key=lambda val: val['node_name'] == 'BUTTON')
    table.sort(key=lambda val: val['node_name'] == 'INPUT', reverse=True)
    return tuple(table)
