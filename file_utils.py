import os
import configparser
from socket import *
import filecmp
import hashlib

def get_url_tuples(walk_dir, postfix = "", filter=".url"):
    file_dict = dict()

    # If your current working directory may change during script execution, it's recommended to
    # immediately convert program arguments to an absolute path. Then the variable root below will
    # be an absolute path as well. Example:
    # walk_dir = os.path.abspath(walk_dir)
    for root, subdirs, files in os.walk(walk_dir):
        for filename in files:
            if filename[-1:-5:-1] == filter[::-1]:
                file_path = os.path.join(root, filename)
                file_dict[filename+postfix] = get_url(file_path)
    return file_dict


def get_file_names(walk_dir, filter=".txt"):
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

def files_are_equal(file_name, old_dir, new_dir):
    old_file = old_dir + '/' + file_name
    new_file = new_dir + '/' + file_name
    #os.path.exists(old_file) and
    #res =  filecmp.cmp(old_file, new_file, shallow=False)

    old_hash=content_hash(old_file)
    new_hash=content_hash(new_file)
    res = old_hash == new_hash
    return res
