# -*- coding: utf8 -*
from time import sleep

from keyboard_and_mouse_tools import get_cursor_pos, get_window_rect
from toolbox import log_record


def cursor_pos(main_data:object):
    win_rect = main_data.win_rect()
    if len(win_rect) == 4:
        x = str(win_rect[0])
        y = str(win_rect[1])
        z = str(win_rect[2])
        w = str(win_rect[3])
    else:
        x = ''
        y = ''
    pos = get_cursor_pos()
    if len(pos) == 2:
        x_pos = str(pos[0])
        y_pos = str(pos[1])
    else:
        x_pos = ''
        y_pos = ''
    try:
        print('окно: '+ x + ',' + y + ',' + z + ',' + w + '   коорд. курсора: '+ x_pos + ',' + y_pos)
    except:
        log_record('не удалось вывести позицию курсора')
    sleep(1)
    cursor_pos(main_data)