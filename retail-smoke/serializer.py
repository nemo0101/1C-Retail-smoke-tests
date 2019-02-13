# -*- coding: utf8 -*
from pickle import dump, load
import logging

from os import (
    path,
    listdir,
    remove,
    curdir
    )

from toolbox import (
        try_except_log,
        try_except_log_ret,
        log_record)


'''
сохраняет кортежи в файлы в папке с программой
'''


def start_swith_filter(template_text:str, filename_text:str):
        if template_text in filename_text:
                result = True
        else:
                result = False
        return result


def get_filenames_in_curdir(text:str, current_dir):
        result = []
        files = try_except_log_ret(listdir, current_dir)
        for x in files:
                if start_swith_filter(text, x):
                        result.append(x)
        return tuple(result)


def remove_files(files:tuple, current_dir):
        for i in files:
                file_dir = current_dir + '\\' + i
                try:
                        remove(file_dir)
                except:
                        log_record('не удалось удалить файл: ' + str(file_dir))


def write_serialize_data(text:str, data, remove_arg=True):
        current_dir = try_except_log_ret(path.abspath, curdir)
        if remove_arg:
                files = get_filenames_in_curdir(text, current_dir)
                if files:
                        remove_files(files, current_dir)
        with open(text+'.pickle', 'wb') as f:
                try_except_log(dump, data, f)


def open_load_file(files:tuple):
        data = None
        for i in files:
                with open(i, 'rb') as f:
                        data = try_except_log_ret(load,f)
        return data


def read_serialize_data(text:str, remove_arg=True):
        current_dir = try_except_log_ret(path.abspath, curdir)
        files = get_filenames_in_curdir(text, current_dir)
        if files != None:
                data = open_load_file(files)
                if remove_arg:
                        remove_files(files, current_dir)
        else: 
                data = None
        return data


def delete_screens_and_log():
        current_dir = try_except_log_ret(path.abspath, curdir)
        screens = get_filenames_in_curdir('screen_', current_dir)
        log_txt = get_filenames_in_curdir('log', current_dir)
        dict_main_elements = get_filenames_in_curdir('dict_main_elements', current_dir)
        if len(screens) > 0:
                remove_files(screens, current_dir)
        if len(log_txt) > 0:
                logging.shutdown()
                remove_files(log_txt, current_dir)
        if len(dict_main_elements) > 0:
                remove_files(dict_main_elements, current_dir)