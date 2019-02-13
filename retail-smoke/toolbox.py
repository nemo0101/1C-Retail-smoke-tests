# -*- coding: utf8 -*
from win32clipboard import (
    OpenClipboard,
    EmptyClipboard,
    SetClipboardText,
    CloseClipboard,
    CF_UNICODETEXT
    )

from sys import exit
from time import ctime
import logging


'''
модуль с дополнительными функциями
'''


def log_record(record:str):
    try:
        logging.basicConfig(filename="log_record.log", level=logging.INFO)
        logging.info(
            (
                str(ctime()),
            ' --- ' + record + ' ---'
            )
        )
    except:
        pass


def try_except_log(function, *args):
    try:
        function(*args)
    except:
        log_record('не сработала функция: ' + str(function))


def try_except_log_ret(function, *args):
    try:
        result = function(*args)
    except:
        log_record('не сработала функция: '+str(locals()['function']))
        result = None
    return result


def copy_to_clipboard(text:str):
    try:
        OpenClipboard()
        EmptyClipboard()
        SetClipboardText(text, CF_UNICODETEXT)
        CloseClipboard()
    except:
        log_record('не удалось поместить данные в clipboad')


def exit_prog():
    exit()
    log_record('программа завершила свою работу')


def cons_input():
    try:
        data = input('>>>: ')
    except:
        log_record('не удалось получить данные из input')
        data = None
    return data


def parse_data_input(data:str):
    if data != None:
        data_list = data.split(',')
        data_list = [i.strip() for i in data_list]
    return tuple(data_list)


def print_string(massage:str):
    try:
        print('>>>: ' + massage)
    except:
        log_record('не удалось вывести сообщение в консоль')
