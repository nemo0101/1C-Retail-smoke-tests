# -*- coding: utf8 -*
from time import sleep

from webdriver import (get_main_or_section_menu, 
                       get_webdriver_quit, 
                       get_page, 
                       wait_window,
                       find_one_element_by_id,
                       find_many_elements_by_tag_name,
                       get_info_from_element,
                       get_the_number_of_pages,
                       get_elem_rect)
from parse_webelements import (parse_elements_by_text,
                               fix_text_matches,
                               parse_elements_on_page,
                               rec_search_last_open_table,
                               sort_table)
from keyboard_and_mouse_tools import (push_button_on_keyboard,
                                      save_screenshot,
                                      simple_click,
                                      simple_enter_text,
                                      search_element_pos)
from toolbox import log_record, exit_prog, setup_key_for_table, setup_existing_key_for_table
from serializer import read_serialize_data, write_serialize_data
from init_program import reload


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
            sleep(2)
            save_screenshot()
            element_box_1 = find_one_element_by_id(main_data.driver(), 'messageBoxTable')
            element_box_2 = find_one_element_by_id(main_data.driver(), 'ps2formContent')
            elements = parse_elements_on_page(
                        find_many_elements_by_tag_name(element_box_1, 'button')
            ) 
            elements += parse_elements_on_page(
                        find_many_elements_by_tag_name(element_box_2, 'span')
            )
            buttons_list_text = []
            buttons_list = []
            for i in elements:
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
                    if i == 'OK' or i == 'Продолжить'  or i == 'Закрыть':
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
                get_webdriver_quit(main_data.driver())
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
            sleep(2)
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
    
    table = setup_key_for_table(
                fix_text_matches(
                    parse_elements_by_text(
                        get_main_or_section_menu(
                            main_data.driver(), main_data.mainmenu()
                        )
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
        table = setup_key_for_table(
                            fix_text_matches(
                                parse_elements_by_text(
                                    get_main_or_section_menu(
                                        main_data.driver(), 
                                        main_data.sectionmenu()
                                    )
                                )
                            )
                        )
        fill_the_table(
            dict_element['table'],
            main_data.driver(),
            table
        )
    return main_data


def menu_full_cycle_go(main_data:object):
    '''
    запускает построение таблицы меню и таблиц вложенных в ее разделы
    возвращает построенную таблицу в объекте
    '''
    return get_table_section_menu(
                get_table_main_menu(main_data)
    )


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
            if x['node_name'] == dict_element['node_name'] and\
               x['text_elem'] == dict_element['text_elem'] and\
               x['rect_elem'] == dict_element['rect_elem']:
                flag_equal = True
                break
        if flag_equal == True:
            old_table_append(dict_element)
            flag_equal = False
            continue
        else:
            new_table_append(dict_element)
    new_table = setup_key_for_table(tuple(new_table))
    key = new_table[0]['key_table']
    old_table = setup_existing_key_for_table(key, tuple(old_table))
    current_table['table'] = new_table
    current_table['context_tables'] += old_table
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


def get_current_page(driver:object, tags_elem:tuple):
    '''
    получает таблицу текущей открытой страницы
    возвращаемый кортеж из трех элементов:
    '''
    current_pages_len = get_the_number_of_pages(driver)
    table_elements = sort_table(
                            parse_elements_on_page(
                                get_page(driver, tags_elem)
                            )
                        )
    return {
        'table':table_elements, 
        'len_table':len(table_elements), 
        'number_of_pages':current_pages_len, 
        'context_tables':tuple()
    }


def compare_table(base_table:dict, main_data:object):
    '''
    в зависимости от количества элементов прошлой, в базе, 
    текщей страницы решает,
    что вернуть в качестве новой таблицы.
    '''
    page_opt = (main_data.page(), main_data.elements(),)
    current_page = get_current_page(main_data.driver(), page_opt)
    res_flag = compare_page_len(base_table, current_page)
    if res_flag == 1:
        result_table = current_page
    elif res_flag == 0.5:
        result_table = eval_new_table(base_table, current_page)
    else:
        result_table = None
    return (res_flag, result_table,)


def return_by_the_click_map(main_data:object, key:float):
    '''
    получает карту из последних нажатых элементов в каждой таблице 
    вплоть до таблици с ключом key
    последовательно нажимает эти элементы
    '''
    log_record('восстановление таблицы')
    click_map = rec_search_last_open_table(main_data.table_elements(), key)

    len_click_map = len(click_map)
    if len_click_map > 0:
        push('esc', len_click_map, main_data)
        for dict_element in click_map:
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


def auxiliary_check_cycle(main_data:object, table, dict_element, limit):
    limit -= 1
    if limit == 0:
        log_record('не удалось вернутся к требуемой таблице, работа приложения прекращена')
        get_webdriver_quit(main_data.driver())
        exit_prog()
    log_record('сравнение таблиц')
    result_table = compare_table(table, main_data)
    if result_table[0] != 0:
        return_by_the_click_map(main_data, dict_element['key_table'])
        auxiliary_check_cycle(main_data, table, dict_element, limit)
        dict_element['click'] = True
        click_or_enter_text(dict_element, main_data)
    else:
        dict_element['click'] = True
        click_or_enter_text(dict_element, main_data)


def cycle(table:dict, main_data:object, switch_click_map = False):
    '''
    рекурсивная функция обхода таблиц.
    '''
    for index, dict_element in enumerate(table['table']):
        '''
        если в каталоге программы присутствует файл data_memory.pickle
        обход начинается с того места где прервался при прошлом запуске
        '''
        if switch_click_map == True:
            if dict_element['click'] == False:
                last_item = table['table'][index - 1]
                if len(last_item['table']['table']) > 0:
                    simple_click(main_data, last_item)
                    table = cycle(last_item['table'], main_data, True)
            else:
                continue
        '''
        далее программа нажимает на каждый элемент в таблице, если при нажатии
        открывается новая страница, программа формирует таблицу и помещает ее к элементу.
        '''
        write_serialize_data('data_memory', main_data.table_elements())
        if dict_element['click'] == False:
            '''
            оценка результата предыдущего нажатия
            '''
            log_record('сравнение таблиц')
            result_table = compare_table(table, main_data)
            '''
            принятие решения согласно оценке
            '''
            if index != 0:
                previous_dict_element = table['table'][index - 1]
            else:
                previous_dict_element = dict_element

            if result_table[0] == 1:
                previous_dict_element['table'] = result_table[1]

                subordinate_table = cycle(previous_dict_element['table'], main_data)

                previous_dict_element['table'] = subordinate_table
                push('esc', 1, main_data)
                auxiliary_check_cycle(main_data, table, dict_element, 5)

            elif result_table[0] == 0.5:
                previous_dict_element['table'] = result_table[1]

                subordinate_table = cycle(previous_dict_element['table'], main_data)

                previous_dict_element['table'] = subordinate_table
                push('esc', 1, main_data)
                auxiliary_check_cycle(main_data, table, dict_element, 5)

            elif result_table[0] == 0:
                dict_element['click'] = True
                click_or_enter_text(dict_element, main_data)

            elif result_table[0] == -1:
                auxiliary_check_cycle(main_data, table, dict_element, 5)

            elif result_table[0] == -0.5:
                auxiliary_check_cycle(main_data, table, dict_element, 5)
    return table


def go_section_menu(dict_element:dict, main_data:object):
    '''
    начинает обход по меню разделов
    '''
    dict_element['click'] = True
    for x in dict_element['table']['table']:
        if x['click'] == False:
            click_or_enter_text(dict_element, main_data)
            x['click'] = True
            click_or_enter_text(x, main_data)
            result_table = compare_table(dict_element['table'], main_data)
            if result_table[0] == 1:
                x['table'] = result_table[1]

                table = cycle(x['table'], main_data)

                if main_data.table_opt() == 'Yes':
                    x['table'] = table
                elif main_data.table_opt() == 'No':
                    x['table'] = {'table':tuple(), 'len_table':0, 'number_of_pages':0, 'context_tables':tuple()}


def go_menu(main_data:object, start_flag:str):
    '''
    начинает обход по главному меню
    '''
    if start_flag == 'start_main':
        main_table = main_data.table_elements()['table']
        for dict_element in main_table:
            if dict_element['click'] == False:
                go_section_menu(dict_element, main_data)
    elif start_flag == 'start_click_map':
        table = cycle(main_data.table_elements(), main_data, True)


def page_full_cycle_go(main_data:object):
    '''
    выбирает метод обхода: либо с сохраненного места (data_memory.pickle) либо с начала
    '''
    data_memory = read_serialize_data('data_memory', False)
    if data_memory != None and len(data_memory['table']) > 0:
        main_data.set_table_elements(data_memory)
        go_menu(main_data, 'start_click_map')
    else:
        go_menu(main_data, 'start_main')
