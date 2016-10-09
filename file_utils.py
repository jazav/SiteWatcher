import configparser
from socket import *
import hashlib
import logging
import os

def get_url_tuples(walk_dir, postfix, filter):
    file_dict = dict()

    # If your current working directory may change during script execution, it's recommended to
    # immediately convert program arguments to an absolute path. Then the variable root below will
    # be an absolute path as well. Example:
    # walk_dir = os.path.abspath(walk_dir)
    for root, subdirs, files in os.walk(walk_dir):
        for file_name in files:
            if file_name[-1:-5:-1] == filter[::-1]:
                file_path = os.path.join(root, file_name)
                full_file_name = file_name + postfix
                file_dict[full_file_name] = get_url(file_path)
    return file_dict


def get_file_names(walk_dir, filter = ".txt"):
    file_list = list()

    # If your current working directory may change during script execution, it's recommended to
    # immediately convert program arguments to an absolute path. Then the variable root below will
    # be an absolute path as well. Example:
    # walk_dir = os.path.abspath(walk_dir)
    for root, subdirs, files in os.walk(walk_dir):
        for filename in files:
            if filename[-1:-5:-1] == filter[::-1]:
                file_list.append(filename)
    return file_list


def get_url(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config['InternetShortcut']['URL']

#with open('some_file_1.txt', 'r') as file1:
#    with open('some_file_2.txt', 'r') as file2:
#        same = set(file1).intersection(file2)#
#
#same.discard('\n')
#
#with open('some_output_file.txt', 'w') as file_out:
#    for line in same:
#        file_out.write(line)


def content_hash(file_name):
    return hashlib.md5(open(file_name,'rb').read()).hexdigest()

def is_html_equal(html1, html2):
    return html1 == html2

def is_file_content_equal(file1, file2):
    with open(file1, "rt") as file_1:
        cont1 = file_1.read()

    with open(file2, "rt") as file_2:
        cont2 = file_2.read()

    return cont1 == cont2

def files_are_equal(file_name, old_dir, new_dir):

    old_file = old_dir + '/' + file_name
    new_file = new_dir + '/' + file_name

    if (not os.path.exists(old_file)):
        logging.info('file: ' + old_file + ' not found')
        return False

    if (not os.path.exists(new_file)):
        logging.info('file: ' + new_file + ' not found')
        return False

    #os.path.exists(old_file) and
    #res =  filecmp.cmp(old_file, new_file, shallow=False)

    ##old_hash=content_hash(old_file)
    #new_hash=content_hash(new_file)

    compare_res = is_file_content_equal(old_file, new_file)

    return compare_res
