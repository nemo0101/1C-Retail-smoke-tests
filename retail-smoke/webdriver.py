# -*- coding: utf8 -*
from selenium import webdriver

from time import sleep

from toolbox import log_record


'''
модуль с функциями связанными с фреймворком selenium
'''


def get_filter_string(flag:str):
    filter_for_span_a_button_only = "@id != contains(@id, 'КоманднаяПанель') and \
                                        @id != contains(@id, 'КнопкаПечать') and \
                                        @id != contains(@id, 'КнопкаВыбора') and \
                                        @id != contains(@id, 'Органайзер') and \
                                        @id != contains(@id, 'ПодменюСоздатьНаОсновании') and \
                                        @id != contains(@id, 'CloseButton') and \
                                        @id != contains(@id, 'NavigateBackButton') and \
                                        @id != contains(@id, 'NavigateForwardButton') and \
                                        @id != contains(@id, 'Справка') and \
                                        @id != contains(@id, 'ПредварительныйПросмотр') and \
                                        @id != contains(@id, 'panelClose') and \
                                        @id != contains(@id, 'ECSFormButton') and \
                                        @id != contains(@id, 'NavigateHomeButton') and \
                                        @id != contains(@id, 'navigateButtons') and \
                                        @id != contains(@id, 'РазвернутьСвернутьТЧ') and \
                                        @id != contains(@id, 'GetURLButton') and \
                                        @id != contains(@id, 'CalculatorButton') and \
                                        @id != contains(@id, 'CalendarButton') and \
                                        @id != contains(@id, 'SetBuffButton') and \
                                        @id != contains(@id, 'AddBuffButton') and \
                                        @id != contains(@id, 'SubBuffButton') and \
                                        @id != contains(@id, 'ScaleFormButton') and \
                                        @id != contains(@id, 'ToolbarMaxMinButton')"

    filter_for_div_only = "contains(@id, 'text_div') or \
                            contains(@id, 'title_text') or \
                            contains(@id, 'Подсистема') or \
                            contains(@id, 'Группа') or \
                            contains(@id, 'thpage')"

    filter_for_div_only_for_main = "contains(@id, 'themesCell')"
    filter_for_div_only_for_section = "contains(@id, 'cmd_')"
    
    filter_div = ".//div[" + filter_for_div_only + "]"
    filter_span = ".//span[@id != '' and " + filter_for_span_a_button_only + "]"
    filter_input = ".//input[@id != '']"
    filter_button = ".//button[@id != '' and " + filter_for_span_a_button_only + "]"
    filter_textarea = ".//textarea[@id != '']"
    filter_label = ".//label[@id != '']"
    filter_a = ".//a[@id != '' and " + filter_for_span_a_button_only + "]"
    
    filter_for_main = ".//div[" + filter_for_div_only_for_main + "]"
    filter_for_section = ".//div[" + filter_for_div_only_for_section + "]"
    filter_all = filter_div + " | " + filter_span + " | " + filter_input + " | " + filter_button + " | " + filter_textarea + " | " + filter_label + " | " + filter_a

    if flag == 'main':
        return_str = filter_for_main
    elif flag == 'section':
        return_str = filter_for_section
    else:
        return_str = filter_all
    return return_str


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
        #log_record('не удалось получить элемент по id: ' + id_str)
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


def find_many_elements_by_part_id(element:object, part_id_str:str, node_context:str):
    try:
        elements = element.find_elements_by_xpath(".//" + node_context + "[contains(@id," + part_id_str + ")]")
        tuple(elements)
    except:
        log_record('не удалось получить элементы по id: ' + part_id_str)
        elements = tuple()
    return elements


def find_many_elements_by_xpath(driver_or_element, xpath:str):
    try:
        elements = driver_or_element.find_elements_by_xpath(xpath)
        tuple(elements)
    except:
        log_record('не удалось получить элементы по xpath')
        elements = tuple()
    return elements


def webdriver_get_window_rect(driver:object):
    try:
        window_rect = driver.get_window_rect()
    except:
        log_record('не удалось получить размер окна браузера')
        window_rect = None
    return window_rect


def get_page(driver:object, menu_flag:str):
    if menu_flag == 'main':
        elements = find_many_elements_by_xpath(
            find_one_element_by_id(driver, 'themesCellLimiter'), 
            get_filter_string(menu_flag)
        )
    elif menu_flag == 'section':
        elements = find_many_elements_by_xpath(
            find_one_element_by_id(driver, 'funcPanel_panelCnt'), 
            get_filter_string(menu_flag)
        )
    else:
        elements = find_many_elements_by_xpath(
            find_one_element_by_id(driver, 'pages_container'), 
            get_filter_string(menu_flag)
        )
    return elements


def wait_window(driver:object, id_str:str, counter:int):
    result = False
    for i in range(counter):
        element = find_one_element_by_id(driver, id_str)
        if element != None:
            result = True
            break
        sleep(0.2)
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


def get_info_from_element(element:object):
    '''
    функция берет данные из элемента и возвращает словарь:
    {
        'id_elem':id_elem - id элемента
        'node_name':node_name, - значение тэга элемента
        'text_elem':text_elem, - текст внутри элемента
        'rect_elem':rect_elem, - словарь размеров и координат элементов 
        'table': None - содержит кортеж новых словарей с элементами которые появились после нажатия на данный элемент
    }
    '''
    dict_elem = None
    if check_is_displayed(element) == True:
        rect_elem = get_elem_rect(element)
        if rect_elem != None and rect_elem['y'] != 0:
            dict_elem = {
                'id_elem':get_elem_id(element),
                'node_name':get_elem_nodname(element),
                'text_elem':get_elem_text(element),
                'rect_elem':rect_elem,
                'table': {'dir':tuple(), 'table':tuple(), 'len_table':0, 'number_of_pages':0, 'context_tables':tuple()}
            }
    return dict_elem
