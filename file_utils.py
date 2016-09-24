import os
import configparser

def get_files_names(walk_dir):

    file_name_lst = list()

    # If your current working directory may change during script execution, it's recommended to
    # immediately convert program arguments to an absolute path. Then the variable root below will
    # be an absolute path as well. Example:
    # walk_dir = os.path.abspath(walk_dir)
    for root, subdirs, files in os.walk(walk_dir):

        for filename in files:
            if filename[-1:-5:-1] == ".url"[::-1]:
                file_path = os.path.join(root, filename)
                file_name_lst.append(file_path)

    return file_name_lst


def get_url(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config['InternetShortcut']['URL']
