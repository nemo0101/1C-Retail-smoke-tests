# -*- coding: utf8 -*


'''
класс для работы с объектами, таблицами и настройками
необходимыми на протяжении всей "жизни" программе
'''

class MainData():

    def __init__(self, tuple_main_data:tuple):
        self.__driver = tuple_main_data[0]
        self.__wscript_shell = tuple_main_data[1]
        self.__option = tuple_main_data[2]
        self.__hwnd = None
        self.__win_rect = None

        self.__mode = self.__search_option('mode', self.__option)
        self.__base_url = self.__search_option('base_url', self.__option)
        self.__coordinate_offset = self.__search_option('coordinate_offset', self.__option)
        self.__auth_win = self.__search_option('auth_win', self.__option)
        self.__win_1c_head = self.__search_option('win_1c_head', self.__option)
        self.__table_opt = self.__search_option('table_opt', self.__option)
        self.__enter_text = self.__search_option('enter_text', self.__option)
        self.__login_opt = self.__search_option('login', self.__option)
        self.__passw_opt = self.__search_option('password', self.__option)
        self.__ok_button_opt = self.__search_option('ok', self.__option)
        self.__del_screen_and_log = self.__search_option('del_screen_and_log', self.__option)

        self.__table_elements = {
            'dir':tuple(),
            'table':tuple(), 
            'len_table':0, 
            'number_of_pages':0, 
            'context_tables':tuple()
        }


    def __search_option(self, option:str, tuple_options:tuple):
        result = None
        if isinstance(tuple_options, tuple):
            for i in tuple_options:
                if len(i) < 2:
                    continue
                if i[0] == option:
                    result = i[1]
                    break
        return result


    def set_hwnd(self, hwnd):
        try:
            hwnd = int(hwnd)
        except:
            hwnd = None
        self.__hwnd = hwnd


    def set_win_rect(self, win_rect):
        if len(win_rect) == 4:
            self.__win_rect = win_rect


    def set_table_elements(self, dict_main_elements):
        self.__table_elements = dict_main_elements


    driver = lambda self: self.__driver
    hwnd = lambda self: self.__hwnd 
    wscript_shell = lambda self: self.__wscript_shell
    mode = lambda self: self.__mode
    base_url = lambda self: self.__base_url
    coordinate_offset = lambda self: self.__coordinate_offset
    auth_win = lambda self: self.__auth_win
    win_1c_head = lambda self: self.__win_1c_head
    table_opt = lambda self: self.__table_opt
    enter_text = lambda self: self.__enter_text
    login_opt = lambda self: self.__login_opt
    passw_opt = lambda self: self.__passw_opt
    ok_button_opt = lambda self: self.__ok_button_opt
    win_rect = lambda self: self.__win_rect
    del_screen_and_log = lambda self: self.__del_screen_and_log

    table_elements = lambda self: self.__table_elements
