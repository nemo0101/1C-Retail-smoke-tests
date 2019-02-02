# -*- coding: utf8 -*
from selenium import webdriver

from time import sleep

from toolbox import log_record, try_except_log_ret

'''
модуль с функциями связанными с фреймворком selenium
'''

def get_webdriver():
    try:
        driver = webdriver.Chrome()
    except:
        driver = None
    return driver


def get_webdriver_quit(driver:object):
    try:
        driver.quit()
    except:
        log_record('не удалось закрыть webdriver')


def open_url(driver:object, url:str):
    try:
        driver.get(url)
    except:
        get_webdriver_quit(driver)
        log_record('не удалось открыть url: ' + url)
    return driver


def find_one_element_by_id(driver:object, id_str:str):
    try:
        element = driver.find_element_by_id(id_str)
    except:
        log_record('не удалось получить элемент по id: ' + id_str)
        element = None
    return element


def find_many_elements_by_tag_name(driver_or_element, tag_name:str):
    try:
        elements = driver_or_element.find_elements_by_tag_name(tag_name)
        tuple(elements)
    except:
        log_record('не удалось получить элементы по tag_name: ' + tag_name)
        elements = tuple()
    return elements


def webdriver_get_window_rect(driver:object):
    try:
        window_rect = driver.get_window_rect()
    except:
        log_record('не удалось получить размер окна браузера')
        window_rect = None
    return window_rect


def get_main_or_section_menu(driver:object, option:tuple):
    return find_many_elements_by_tag_name(
        find_one_element_by_id(driver, option[0]), 
        option[1]
    )


def get_page(driver:object, option:tuple):
    list_of_all_elements = tuple()
    for x in option[1]:
        elements = find_many_elements_by_tag_name(
                        find_one_element_by_id(driver, option[0]), 
                        x
        )
        list_of_all_elements += tuple(elements)
    return list_of_all_elements


def wait_window(driver:object, id_str:str, counter:int):
    result = False
    for i in range(counter):
        element = find_one_element_by_id(driver, id_str)
        if element:
            result = True
            break
        sleep(1)
    return result


def get_the_number_of_pages(driver:object):
    elements = find_many_elements_by_tag_name(
        find_one_element_by_id(driver, 'openedCell_cont'), 'div'
    )
    return len(elements)


def webelement_click(driver:object, element:dict):
    if isinstance(element, dict):
        webelement = find_one_element_by_id(driver, element['id_elem'])
        try:
            flag = True
            webelement.click()
            log_record('активация элемента: ' + element['text_elem'])
        except:
            flag = False
        return flag


def webelement_enter_text(driver:object, element:dict, text:str):
    if element != None:
        webelement = find_one_element_by_id(driver, element['id_elem'])
        try:
            flag = True
            webelement.send_keys(text)
        except:
            flag = False
        return flag


def check_div(id_text:str):
    '''
    выбирает разрешенные элементы div по части иx id
    '''
    flag = False
    if 'text_div' in id_text or\
    'title_text' in id_text or\
    'Подсистема' in id_text or\
    'Группа' in id_text or\
    'thpage' in id_text:
        flag = True
    return flag


def filter_for_page(node_name:str, text_elem:str, id_elem:str):
    flag = False
    if node_name == '' or \
       id_elem == '' or\
       node_name == 'DIV' and text_elem == '' or \
       node_name == 'DIV' and check_div(id_elem) == False or \
       node_name == 'SPAN' and text_elem == '':
        flag = True
    return flag


def filter_for_main_menu(node_name:str, text_elem:str, id_elem:str):
    flag = True
    if node_name != '' and \
       node_name == 'DIV' and text_elem != '' and \
       node_name == 'DIV' and 'cmd_' in id_elem or \
       node_name == 'DIV' and 'themesCell' in id_elem or \
       node_name == 'SPAN' and text_elem != '':
        flag = False
    return flag


def cheсk_in_except_table(text_el:str, id_el:str):
    '''
    фильтрует элементы которые не нужны
    '''
    flag = False
    if text_el == 'Еще' or \
       text_el == 'Печать' or \
       'КнопкаПечать' in id_el or\
       'ПодменюСоздатьНаОсновании' in id_el or \
       'CloseButton' in id_el == True or \
       'NavigateBackButton' in id_el or \
       'NavigateForwardButton' in id_el or \
       'Справка' in id_el or \
       'ПредварительныйПросмотр' in id_el or \
       'panelClose' in id_el or\
       'ECSFormButton' in id_el or\
       'NavigateHomeButton' in id_el or\
       'navigateButtons' in id_el or\
       'РазвернутьСвернутьТЧ' in id_el:
        flag = True
    return flag


def check_is_displayed(element:object):
    try:
        is_displayed = element.is_displayed()
    except:
        is_displayed = False
    return is_displayed


def get_elem_rect(element:object):
    try:
        rect_elem = element.rect
    except:
        rect_elem = None
    return rect_elem


def get_elem_nodname(element:object):
    try:
        node_name = element.get_attribute('nodeName')
    except:
        node_name = ''
    return node_name


def get_elem_text(element:object):
    try:
        text_elem = element.text
    except:
        text_elem = ''
    return text_elem


def get_elem_id(element:object):
    try:
        id_elem = element.get_attribute('id')
    except:
        id_elem = ''
    return id_elem


def get_info_from_element(element:object, filter_mode='filter_for_page'):
    '''
    функция берет данные из элемента и возвращает словарь:
    {
        'key_table':None, - идентификатор таблицы сгенирированный из случайных чисел
        'id_elem':id_elem - id элемента
        'node_name':node_name, - значение тэга элемента
        'text_elem':text_elem, - текст внутри элемента
        'rect_elem':rect_elem, - словарь размеров и координат элементов 
        'click': False, - параметр обозначающий было ли произведено нажатие на элемент
        'table': None - содержит кортеж новых словарей с элементами которые появились после нажатия на данный элемент
    }
    '''
    dict_elem = None
    if check_is_displayed(element) == True:
        rect_elem = get_elem_rect(element)
        if rect_elem != None and rect_elem['y'] != 0:
            node_name = get_elem_nodname(element)
            text_elem = get_elem_text(element)
            id_elem = get_elem_id(element)
            if filter_mode == 'filter_for_page':
                res_filter = filter_for_page(node_name, text_elem, id_elem)
            elif filter_mode == 'filter_for_main_menu':
                res_filter = filter_for_main_menu(node_name, text_elem, id_elem)
            if res_filter == False:
                if cheсk_in_except_table(text_elem, id_elem) == False:
                    dict_elem = {
                        'key_table':None,
                        'id_elem':id_elem,
                        'node_name':node_name,
                        'text_elem':text_elem,
                        'rect_elem':rect_elem,
                        'click': False,
                        'table': {'table':tuple(), 'len_table':0, 'number_of_pages':0, 'context_tables':tuple()}
                    }
    return dict_elem
