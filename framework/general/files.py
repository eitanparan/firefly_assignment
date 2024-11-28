import configparser
import json
import os
import shutil

import retry


def create_json_file(json_key_vals, file_name):
    """

    :param json_key_vals:
    :param file_name:
    :return:
    """
    dictionary = json_key_vals
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)
    # Writing to sample.json
    with open(file_name, "w") as outfile:
        outfile.write(json_object)


def delete_file(path):
    """

    :param path:
    :return:
    """
    try:
        os.remove(path)
    except OSError:
        pass


def check_if_file_exist(directory, file_name_contains):
    """

    :param dir:
    :param file_name_contains:
    :return:
    """
    files_names = os.listdir(directory)
    for name in files_names:
        if file_name_contains in name:
            return True


def check_if_directory_exist(dir_path):
    """

    :param dir_path:
    :return:
    """
    try:
        return os.path.exists(dir_path)
    except Exception as err:
        raise Exception(f"Failed to check if dir {dir_path} exists: {err}")


@retry.retry(ValueError, tries=10, delay=6)
def wait_for_file_to_exist(directory=None, file_name_contains=None):
    """

    :param directory:
    :param file_name_contains:
    :return:
    """
    try:
        if check_if_file_exist(directory=directory, file_name_contains=file_name_contains):
            return True
        else:
            raise ValueError(f"File containing {file_name_contains} not found")
    except Exception as err:
        raise ValueError(err)


def delete_directory_contents(dir_path):
    """

    :param dir_path:
    :return:
    """
    try:
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
    except Exception as err:
        raise Exception(f"Failed to delete dir {dir_path} contents: {err}")


def read_ini_file(file_path, section, key):
    """

    :param file_path:
    :param section:
    :param key:
    :return:
    """
    try:
        config = configparser.ConfigParser()
        config.read(file_path)
        return config.get(section, key)
    except Exception as err:
        raise Exception(f"Failed to read ini file {file_path}: {err}")


def map_ini_file_section_key_to_dict(file_path=None, section=None, key=None, required_value_name=None):
    """

    :param file_path:
    :param section:
    :param key:
    :param required_value_name:
    :return:
    """
    try:
        _values = read_ini_file(file_path=file_path, section=section, key=key)
        values = _values.split(' ')
        for index in range(len(values)):
            if values[index] == required_value_name:
                return values[index + 1]
        return None
    except Exception as err:
        raise Exception(f"{"#" * 200}\n{"#" * 200}\nFailed to map ini file section key to dict {file_path}\nPLEASE RUN "
                        f"FROM UNITY FOLDER TO FIX THIS ERROR: {err}{"#" * 200}\n{"#" * 200}\n")


def get_all_files_in_dir(dir_path):
    """

    :param dir_path:
    :return:
    """
    try:
        return os.listdir(dir_path)
    except Exception as err:
        raise Exception(f"Failed to get all files names from path {dir_path}: {err}")


def get_all_workers_files(workers_files_dir_path, string_to_include=None):
    """

    :param workers_files_dir_path:
    :return:
    """
    try:
        workers_files = []
        all_files_in_dir = get_all_files_in_dir(workers_files_dir_path)
        for file in all_files_in_dir:
            if string_to_include in file:
                workers_files.append(file)
        return workers_files
    except Exception as err:
        raise Exception(f"Failed to get all workers files from dir {workers_files_dir_path}: {err}")


def delete_file_if_exist(file_path):
    """

    :param file_path:
    :return:
    """
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
    except Exception as err:
        raise Exception(f"Failed to delete file {file_path}: {err}")


def create_folder_if_doesnt_exist(path):
    """

    :param path:
    :return:
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except Exception as err:
        raise Exception(f"Failed to create folder at path {path}: {err}")


def delete_folder_if_exist(path):
    """

    :param path:
    :return:
    """
    try:
        if os.path.exists(path):
            shutil.rmtree(path)
    except Exception as err:
        raise Exception(f"Failed to create folder at path {path}: {err}")


def read_file(path):
    """
    Reading file with content manager to make sure it's closed after
    :param path: path to file
    :return: file content
    """
    try:
        with open(path, 'r') as file:
            return file.read()
    except Exception as err:
        raise Exception(f"Failed to read file at path {path}: {err}")


def write_line_to_file(file_path, line):
    """
    Writes a line into a file
    :param file_path:
    :param line:
    :return:
    """
    try:
        file = open(file_path, 'w+')
        file.write(line)
    except Exception as err:
        raise Exception(f"failed writing line \"{line}\" to file {file_path}: {err}")
