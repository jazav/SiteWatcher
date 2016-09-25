import os
import configparser
from socket import *



def get_files_names(walk_dir):

    file_name_dict = dict()

    # If your current working directory may change during script execution, it's recommended to
    # immediately convert program arguments to an absolute path. Then the variable root below will
    # be an absolute path as well. Example:
    # walk_dir = os.path.abspath(walk_dir)
    for root, subdirs, files in os.walk(walk_dir):

        for filename in files:
            if filename[-1:-5:-1] == ".url"[::-1]:
                file_path = os.path.join(root, filename)
                file_name_dict[filename] = get_url(file_path)
    return file_name_dict


def get_url(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config['InternetShortcut']['URL']
