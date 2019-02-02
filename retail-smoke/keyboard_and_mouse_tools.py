# -*- coding: utf8 -*
from win32gui import (GetForegroundWindow,
                      SetForegroundWindow,
                      ShowWindow,
                      GetWindowRect,
                      GetWindowText,
                      EnumWindows,
                      SetWindowPos,
                      GetDesktopWindow,
                      GetWindowDC,
                      DeleteObject
                      )
from win32con import (SW_MAXIMIZE,
                      MOUSEEVENTF_LEFTDOWN,
                      MOUSEEVENTF_LEFTUP,
                      MOUSEEVENTF_RIGHTDOWN,
                      MOUSEEVENTF_RIGHTUP,
                      MOUSEEVENTF_WHEEL,
                      SWP_SHOWWINDOW,
                      HWND_TOP,
                      SM_CXVIRTUALSCREEN,
                      SM_CYVIRTUALSCREEN,
                      SM_XVIRTUALSCREEN,
                      SM_YVIRTUALSCREEN,
                      SRCCOPY
                      )
from win32api import (SetCursorPos,
                      mouse_event,
                      GetCursorPos,
                      GetSystemMetrics
                      )
from win32com.client import Dispatch
from win32ui import CreateDCFromHandle, CreateBitmap
from PIL import Image

from time import sleep, ctime

from toolbox import log_record, copy_to_clipboard
from webdriver import (webelement_enter_text, 
                       webelement_click, 
                       get_info_from_element, 
                       find_one_element_by_id)

'''
модуль для работы с мышью и клавиатурой
'''

def return_wscript_shell():
    try:
        shell = Dispatch('WScript.Shell')
    except:
        log_record('не удалось получить WScript.Shell')
        shell = None
    return shell


def get_foreground_window():
    try:
        hwnd = GetForegroundWindow()
    except:
        log_record('не удалось получить окно переднего плана')
        hwnd = None
    return hwnd


def set_foreground_window(hwnd:int):
    try:
        SetForegroundWindow(hwnd)
    except:
        log_record('не удалось вывести окно на передний план')


def full_screen(hwnd:int):
    try:
        ShowWindow(hwnd, SW_MAXIMIZE)
    except:
        log_record('не удалось развернуть окно на полный экран')


def get_window_rect(hwnd:int):
    '''
    получает кортеж с координатами окна
    '''
    try:
        window_rect = GetWindowRect(hwnd)
    except:
        log_record('не удалось получить координаты окна')
        window_rect = list()
    return window_rect


def return_key_for_wscript_shell(key:str):
    buttons = {
        'f4':'{F4}',
        'space':'{ }',
        'down':'{DOWN}',
        'enter':'{ENTER}',
        'next_table':'^{PGDN}',
        'tab':'{TAB}',
        'exit':'^{F4}',
        'go_to_link':'(+{F11})',
        'insert':'{INSERT}',
        'paste':'^v',
        'delete':'{DEL}',
        'select_all':'^a',
        'bksp':'{BKSP}',
        'cntrl_entr':'(^{ENTER})',
        'esc':'{ESC}',
        'close_msg':'^+{z}'
    }
    button_value = None
    for x in buttons.keys():
        if x == key:
            button_value = buttons[x]
            break
    if button_value == None:
        log_record('не удалось получить значение кнопки')
    return button_value


def push_button_on_keyboard(hwnd:int, wscript_shell:object, key:str, count=1):
    key_value = return_key_for_wscript_shell(key)
    if key_value:
        try:
            for x in range(count):
                set_foreground_window(hwnd)
                wscript_shell.SendKeys(key_value)
                log_record('выполнено нажатие: ' + key_value)
                sleep(1)
        except:
            log_record('не удалось нажать на кнопку: ' + key)


def set_cursor_pos(x:int, y:int):
    try:
        SetCursorPos([x, y])
    except:
        log_record('не удалось установить курсор в позицию: ' + str(x) + '/' + str(y))


def mouse_event_func(event):
    try:
        mouse_event(event, 0, 0, 0, 0)
    except:
        log_record('не удалось нажать мышью')


def click(x:int, y:int):
    set_cursor_pos(x, y)
    sleep(1)
    mouse_event_func(MOUSEEVENTF_LEFTDOWN)
    mouse_event_func(MOUSEEVENTF_LEFTUP)


def click_right(x:int, y:int):
    set_cursor_pos(x, y)
    sleep(1)
    mouse_event_func(MOUSEEVENTF_RIGHTDOWN)
    mouse_event_func(MOUSEEVENTF_RIGHTUP)


def search_cord(y, win_rect):
    '''
    возвращает значение флага:
    0 - элемент находится в окне
    1 - элемент выше чем окно
    -1 - элемент ниже чем окно
    '''
    y_upper = win_rect[3] - 10
    y_lower = win_rect[1] + 10
    if y_upper > y and y_lower < y:
        flag = 0
    elif y_upper < y and y_lower < y:
        flag = 1
    elif y_upper > y and y_lower > y:
        flag = -1
    return flag


def scroll(x, y, scroll_count, flag=-1):
    '''
    значения flag:
    -1 - колесо мыши прокручивает вниз на 200
    1 - колесо мыши прокручивает вверх на 200
    '''
    scroll_count = scroll_count*flag
    set_cursor_pos(x, y)
    sleep(0.5)
    mouse_event(MOUSEEVENTF_WHEEL, scroll_count, scroll_count, scroll_count, scroll_count)


def search_element_pos(dict_element, main_data, count=5):
    y = dict_element['rect_elem']['y']
    id_elem = dict_element['id_elem']
    win_rect = main_data.win_rect()
    average_x = win_rect[2] - win_rect[0]
    average_y = win_rect[3] - win_rect[1]
    flag = False
    res_search = search_cord(y, win_rect)
    if res_search == 0:
        flag = True
    else:
        for i in range(count):
            new_elem = get_info_from_element(
                        find_one_element_by_id(main_data.driver(), id_elem)
            )
            x = new_elem['rect_elem']['x']
            y = new_elem['rect_elem']['y']
            id_elem = new_elem['id_elem']
            res_search = search_cord(y, win_rect)
            if res_search == 0:
                flag = True
                break
            if res_search == 1:
                # возможно нужно добавить формулу вычисления от центра
                x = average_x
                y = average_y
                scroll(x, y, 200, 1)
            if res_search == -1:
                x = average_x
                y = average_y
                scroll(x, y, 200, -1)
    return flag


def click_in_test(hwnd:int,
                  element:dict,
                  one_or_two_click:str,
                  coordinate_offset:str, 
                  mouse_click='left'):
    if element != None:
        try:
            coordinate_offset = int(coordinate_offset)
        except:
            log_record('не удалось преобразовать coordinate_offset в число')
        try:
            x = element['rect_elem']['x'] + round(element['rect_elem']['width']/6)
            y = element['rect_elem']['y'] + round(element['rect_elem']['height']/2)+coordinate_offset
        except:
            log_record('не удалось получить данные для нажатия')
        set_foreground_window(hwnd)
        if one_or_two_click == 'one':
            if mouse_click == 'left':
                click(x, y)
            else:
                click_right(x, y)
            log_record('выполнено нажатие: ' + element['text_elem'] + ' координаты: ' + str(x) + ' / ' + str(y))
        elif one_or_two_click == 'two':
                click(x, y)
                sleep(1)
                click(x, y)
                log_record('выполнено двойное нажатие: ' + element['text_elem'] + ' координаты: ' + str(x) + ' / ' + str(y))


def enum_windows(func):
    try:
        EnumWindows(func, 0)
    except:
        log_record('не сработала функция win32gui.EnumWindows()')


def get_all_windows():
    hwnds = []

    def service_func(hwnd:int, param):
        hwnds.append(hwnd)

    enum_windows(service_func)
    return tuple(hwnds)


def search_hwnd(hwnd:int):
    tuple_hwnds = get_all_windows()
    if len(tuple_hwnds) == 0:
        result = False
    else:
        for i in tuple_hwnds:
            if i == hwnd:
                result = True
                break
            else:
                result = False
    return result


def get_window_text(hwnd:int):
    try:
        win_text = GetWindowText(hwnd)
    except:
        log_record('не удалось получить заголовок тестируемого окна')
        win_text = ''
    return win_text


def enter_text(main_data:object, element:dict, text:str):
    click_in_test(
        main_data.hwnd(), 
        element, 
        'two', 
        main_data.coordinate_offset()
    )
    copy_to_clipboard(text)
    push_button_on_keyboard(
        main_data.hwnd(), 
        main_data.wscript_shell(), 
        'paste'
    )


def simple_click(main_data:object, element:dict):
    if webelement_click(
        main_data.driver(), 
        element
        ) == False:
            click_in_test(
                main_data.hwnd(), 
                element, 
                'one', 
                main_data.coordinate_offset()
            )


def simple_enter_text(main_data:object, element:dict, text:str):
    if webelement_enter_text(
        main_data.driver(), 
        element, 
        text
        ) == False:
            enter_text(main_data, 
                       element, 
                       text)


def get_cursor_pos():
    try:
        pos = GetCursorPos()
    except:
        log_record('не удалось получить позицию курсора')
        pos = None
    return pos


def set_window_pos(hwnd, x, y, width, height):
    try:
        SetWindowPos(hwnd, HWND_TOP, x, y, width, height, SWP_SHOWWINDOW)
    except:
        log_record('не удалось установить окно в нужную позицию')


def save_screenshot():
    hwnd = GetDesktopWindow()
    width = GetSystemMetrics(SM_CXVIRTUALSCREEN)
    height = GetSystemMetrics(SM_CYVIRTUALSCREEN)
    x = GetSystemMetrics(SM_XVIRTUALSCREEN)
    y = GetSystemMetrics(SM_YVIRTUALSCREEN)
    
    hwnd_dc = GetWindowDC(hwnd)
    mfc_dc  = CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()

    save_bit_map = CreateBitmap()
    save_bit_map.CreateCompatibleBitmap(mfc_dc, width, height)
    save_dc.SelectObject(save_bit_map)
    save_dc.BitBlt(
        (0, 0), 
        (width, height), 
        mfc_dc, 
        (x, y), 
        SRCCOPY
    )
    
    bmp_info = save_bit_map.GetInfo()
    bmp_str = save_bit_map.GetBitmapBits(True)
    image = Image.frombuffer(
        'RGB', 
        (bmp_info['bmWidth'], bmp_info['bmHeight']), 
        bmp_str, 
        'raw', 
        'BGRX', 
        0, 
        1
    )
    time_str = str(ctime()).replace(' ', '_').replace(':', '_').lower()
    name_scr = 'screen_' + time_str + '.png'
    image.save(name_scr, format = 'png')
    log_record('сохранен скриншот: ' + name_scr)
    save_dc.DeleteDC()
    DeleteObject(save_bit_map.GetHandle())