# -*- coding: utf8 -*
from time import sleep

from webdriver import (get_webdriver_quit, 
                       get_page, 
                       wait_window,
                       find_one_element_by_id,
                       find_many_elements_by_tag_name,
                       get_the_number_of_pages,
                       get_info_from_element)
from parse_webelements import (parse_elements_by_text,
                               fix_text_matches,
                               parse_elements_on_page,
                               sort_table)
from keyboard_and_mouse_tools import (push_button_on_keyboard,
                                      save_screenshot,
                                      simple_click,
                                      simple_enter_text,
                                      search_element_pos)
from toolbox import log_record
from init_program import reload


'''
основная логика работы для режимов savemenu, go, go_partial
'''


def wait_win_1c_head(main_data:object):
    '''
    ждет появления окна 1С:Предприятия
    если окно появляется пытается закрыть его
    если не находит кнопки для закрытия прерывает работу программы
    '''
    if wait_window(
        main_data.driver(), 
        main_data.win_1c_head(), 
        1
        ) == True:
            log_record('обнаружено окно: 1С:Предприятие')
            sleep(5)
            save_screenshot()
            element_box_1 = find_one_element_by_id(main_data.driver(), 'messageBoxTable')
            element_box_2 = find_one_element_by_id(main_data.driver(), 'ps2formContent')
            if element_box_1 == None:
                log_record('не удалось обнаружить окно 1С:Предприятия - завершена работа программы')
                reload(main_data)
            elements = find_many_elements_by_tag_name(element_box_1, 'button')
            elements += find_many_elements_by_tag_name(element_box_2, 'span')
            elements_dict = []
            for x in elements:
                elements_dict.append(get_info_from_element(x))
            if len(elements_dict) == 0:
                log_record('не удалось установить кнопки окна 1С:Предприятия - завершена работа программы')
                reload(main_data)
            buttons_list_text = []
            buttons_list = []
            for i in elements_dict:
                if i['text_elem'] == 'Да' or \
                   i['text_elem'] == 'Нет' or \
                   i['text_elem'] == 'Отмена' or \
                   i['text_elem'] == 'OK' or \
                   'Закрыть' in i['id_elem']:
                    if 'Закрыть' in i['id_elem']:
                        i['text_elem'] = 'Закрыть'
                    buttons_list_text.append(i['text_elem'])
                    buttons_list.append(i)
            res_list = list(
                set(buttons_list_text) & set(['OK', 'Да', 'Нет', 'Отмена', 'Продолжить', 'Закрыть'])
            )

            flag = False
            if flag == False:
                for i in res_list:
                    if i == 'OK' or i == 'Продолжить' or i == 'Закрыть':
                        flag = True
                        for y in buttons_list:
                            if y['text_elem'] == i:
                                simple_click(main_data, y)
                                break
                        break

            if flag == False:
                for i in res_list:
                    if i == 'Отмена':
                        for y in buttons_list:
                            if y['text_elem'] == 'Нет':
                                flag = True
                                simple_click(main_data, y)
                                break
                        break

            if flag == False:
                for i in res_list:
                    if i == 'Да':
                        flag = True
                        for y in buttons_list:
                            if y['text_elem'] == i:
                                simple_click(main_data, y)
                                break
                        break

            if flag == False and element_box_1 != None:
                log_record('не удалось закрыть окно 1С:Предприятия - завершена работа программы')
                reload(main_data)


def wait_msg(main_data):
    '''
    ждет появления сообщения пользователю
    если сообщение появляется пытается закрыть его
    если не находит кнопки для закрытия прерывает работу программы
    '''
    if wait_window(
        main_data.driver(), 
        'msg0', 
        1
        ) == True:
            flag = False
            log_record('обнаружено окно: Сообщить ')
            sleep(5)
            save_screenshot()
            push_button_on_keyboard(main_data.hwnd(), main_data.wscript_shell(), 'close_msg')


def push(key:str, quant:int, main_data):
    for i in range(quant):
        push_button_on_keyboard(main_data.hwnd(), main_data.wscript_shell(), key, 1)
        wait_win_1c_head(main_data)
        wait_msg(main_data)
        reload(main_data)


def fill_the_table(receiving_table, driver, data_table, new_context_tables=tuple()):
    receiving_table['table'] += data_table
    receiving_table['len_table'] = len(data_table)
    receiving_table['number_of_pages'] = get_the_number_of_pages(driver)
    receiving_table['context_tables'] += new_context_tables


def get_table_main_menu(main_data:object):
    '''
    создает таблицу основного меню
    '''
    sleep(1)
    
    table = fix_text_matches(
                parse_elements_by_text(
                    get_page(
                        main_data.driver(), 'main'
                    )
                )
            )
    fill_the_table(
        main_data.table_elements(),
        main_data.driver(),
        table
    )
    return main_data


def get_table_section_menu(main_data:object):
    '''
    в таблицу с главным меню, добавляет
    данные о разделах каждой позиции (добавляет в значение ключа [table] каждого элемента) основного меню
    '''
    main_table = main_data.table_elements()['table']
    for dict_element in main_table:
        simple_click(main_data, dict_element)
        table = fix_text_matches(
                            parse_elements_by_text(
                                get_page(
                                    main_data.driver(), 
                                    'section'
                                )
                            )
                        )
        fill_the_table(
            dict_element['table'],
            main_data.driver(),
            table
        )
    return main_data


def get_current_page(driver:object, tags_elem:tuple):
    '''
    получает таблицу текущей открытой страницы
    возвращаемый кортеж:
    '''
    current_pages_len = get_the_number_of_pages(driver)
    table_elements = sort_table(
                            parse_elements_on_page(
                                get_page(driver, 'page')
                            )
                        )
    return {
        'dir':tuple(),
        'table':table_elements, 
        'len_table':len(table_elements), 
        'number_of_pages':current_pages_len, 
        'context_tables':tuple()
    }


def menu_full_cycle_go(main_data:object):
    '''
    запускает построение таблицы меню и таблиц вложенных в ее разделы
    возвращает построенную таблицу в объекте
    '''
    table = get_table_section_menu(
                get_table_main_menu(main_data)
    )
    push('esc', 1, main_data)
    return table


def eval_new_table(base_table:dict, current_table:dict):
    '''
    если флаг сравнения был 0,5 (на текущей странице добавилось элементов) 
    то вызывается эта функция.
    она сравнивает две таблицы
    если в базовой таблице нет элемента из текущей
    то этот элемент попадает в новую таблицу иначе попадает в старую таблицу
    новая таблица идет и заменяет ['table'] для последующего обхода
    старая таблица идет и добавляется к ['context_tables'] для адекватного сравнения таблиц в дальнейшем
    '''
    base_table['table'] += base_table['context_tables']
    new_table = []
    new_table_append = new_table.append
    old_table = []
    old_table_append = old_table.append
    flag_equal = False
    for dict_element in current_table['table']:
        for x in base_table['table']:
            if x['id_elem'] == dict_element['id_elem']:
                flag_equal = True
                break
        if flag_equal == True:
            old_table_append(dict_element)
            flag_equal = False
            continue
        else:
            new_table_append(dict_element)
    current_table['table'] = tuple(new_table)
    current_table['context_tables'] += tuple(old_table)
    return current_table


def compare_page_len(base_table:dict, current_page:dict):
    '''
    стравнивает данные о количестве страниц в таблице
    с текущим количеством страниц. 
    если количество страниц совпадает, сравнивает первоначальное количество элементов
    текущих данных базы со свежеполученными
    result = 0: новой страницы, модальных окон, выпадающих списков не обнаружено
    result = -1: вернулись на предыдущую страницу
    result = 1: появилась новая страница
    result = 0.5: на той же странице появилось модально окно, выпадающий список и т.д.
    result = -0.5: на той же странице исчезло модально окно, выпадающий список и т.д.
    '''
    result = 0
    if current_page['number_of_pages'] > base_table['number_of_pages']:
        result = 1
    elif current_page['number_of_pages'] < base_table['number_of_pages']:
        result = -1
    elif current_page['number_of_pages'] == base_table['number_of_pages'] and \
         base_table['len_table']  < current_page['len_table']:
        result = 0.5
    elif current_page['number_of_pages'] == base_table['number_of_pages'] and \
         base_table['len_table'] > current_page['len_table']:
        result = -0.5
    elif current_page['number_of_pages'] == base_table['number_of_pages'] and \
         base_table['len_table'] == current_page['len_table']:
        result = 0
    return result


def compare_table(base_table:dict, main_data:object):
    '''
    в зависимости от количества элементов
    текщей страницы решает,
    что вернуть в качестве новой таблицы.
    '''
    current_page = get_current_page(main_data.driver(), 'page')
    res_flag = compare_page_len(base_table, current_page)
    if res_flag == 1:
        result_table = current_page
    elif res_flag == 0.5:
        result_table = eval_new_table(base_table, current_page)
    else:
        result_table = None
    return (res_flag, result_table,)


def return_by_the_click_map(main_data:object, table:tuple):
    '''
    получает путь, состоящий из элементов, который нужно нажать чтобы открыть данную таблицу.
    последовательно нажимает эти элементы
    '''
    len_click_map = len(table['dir'])
    if len_click_map > 0:
        push('esc', len_click_map, main_data)
        for dict_element in table['dir']:
            simple_click(main_data, dict_element)
            sleep(2)


def click_or_enter_text(dict_element:dict, main_data:object):
    '''
    ищет элемент в области окна браузера,
    в зависимотсти от node_name элемента 
    выполняет нажатие, далее срабатывает ожидание окон
    '''
    search_elem = search_element_pos(dict_element, main_data, 5)
    if search_elem:
        if dict_element['node_name'] == 'INPUT':
            simple_enter_text(
                main_data,
                dict_element,
                main_data.enter_text()
            )
        else:
            simple_click(main_data, dict_element)
        wait_win_1c_head(main_data)
        wait_msg(main_data)
        reload(main_data)


def test(curr_table, main_data:object):
    '''
    обход элементов каждой таблицы
    '''
    len_dir_table = len(curr_table['dir'])
    res_table = []
    res_table_append = res_table.append
    for elem in curr_table['table']:
        click_or_enter_text(elem, main_data)
        log_record(elem['id_elem'] + ' / ' + elem['text_elem'])
        #оценка результата нажатия
        log_record('сравнение таблиц')
        result_table = compare_table(curr_table, main_data)
        #принятие решения согласно оценке
        if result_table[0] == 1 or result_table[0] == 0.5:
            result_table[1]['dir'] = curr_table['dir'] + (elem,)
            res_table_append(result_table[1])
            push('esc', len_dir_table, main_data)
            return_by_the_click_map(main_data, curr_table)
        else:
            push('esc', len_dir_table, main_data)
            return_by_the_click_map(main_data, curr_table)
    push('esc', len_dir_table, main_data)
    return tuple(res_table)


def start(main_data:object):
    '''
    основной обход по таблицам. 
    после того как работа с таблицей заканчивается
    ей присваивается значение None
    '''
    table = main_data.table_elements()
    for val in table:
        if val['table'] != None:
            return_by_the_click_map(main_data, val)
            table += test(val, main_data)

            val['dir'] = None
            val['table'] = None
            val['len_table'] = None
            val['number_of_pages'] = None
            val['context_tables'] = None


def get_page_info(main_data:object, x:dict, y:dict):
    '''
    собирает данные со страниц
    выстраивает пути к ним
    '''
    simple_click(main_data, x)
    simple_click(main_data, y)
    table = get_current_page(
                main_data.driver(), 
                'page'
    )
    table['dir'] += (x, y,)
    push('esc', 2, main_data)
    return table


def go_menu(main_data:object):
    '''
    первый поверхностный обход
    '''
    list_curr_table = []
    list_curr_table_append = list_curr_table.append
    for x in main_data.table_elements()['table']:
        for y in x['table']['table']:
            list_curr_table_append(
                get_page_info(main_data, x, y)
            )
    main_data.set_table_elements(tuple(list_curr_table))
    start(main_data)


def page_full_cycle_go(main_data:object):
    '''
    выбирает метод обхода: либо с сохраненного места (data_memory.pickle) либо с начала
    '''
    go_menu(main_data)
