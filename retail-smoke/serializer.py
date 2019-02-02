# -*- coding: utf8 -*
from pickle import dump, load

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
        try:
                result = filename_text.startswith(template_text)
        except:
                log_record('не удалось проверить начинается ли файл с заданного шаблона')
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
                try_except_log(remove, file_dir)


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