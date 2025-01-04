import csv
import json
import os
from typing import Any

from custom_types.custom_types import CSVData


def extract_csv_data(file_name: str) -> CSVData:
    """Returns the contents of the csv file as a list"""
    with open(file_name, "r") as csv_file:
        data = list(csv.reader(csv_file))
    return data


def extract_json_data(file_name: str) -> Any:
    """Returns the contents of the json file."""
    if os.path.exists(file_name):
        with open(file_name, "r") as file_obj:
            data = json.load(file_obj)
    else:
        data = {}
    return data


def extract_data(file_name: str) -> Any:
    """Returns the contents of the file (csv or json)"""
    # TODO - enforce only json or csv
    data_type = os.path.splitext(file_name)[-1]

    if data_type == ".json":
        return extract_json_data(file_name)
    else:
        return extract_csv_data(file_name)


def zip_csv_files(src: str, dest: str, delete_input_files: bool) -> None:
    """
    Merges the csv files in scr and saves them to dest. Can delete
    the files and removes the 1st row from each file (assumed to be
    a header).
    """
    input_files = os.listdir(src)

    with open(dest, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)

        for file in input_files:
            full_file_path = os.path.join(src, file)
            data = extract_data(full_file_path)
            csv_writer.writerows(data[1:])
            if delete_input_files:
                os.remove(full_file_path)
    return


def is_subpath(fp: str) -> bool:
    """
    Returns true if the given file path starts in the src directory

    Args:
        fp (str): the filepath to be checked

    Returns:
        bool: true if the given file path beings with the src file path
    """
    return fp.startswith(os.path.dirname(os.path.dirname(__file__)))


def save_json_data(fp: str, data: Any) -> None:
    """
    Saves the provided data to a json file. If the given file path is
    not within the project root, an error is raised. All required
    directories are created if they do not exist.

    Args:
        fp (str): the filepath
        data: the data to be saved in the json file
    """
    if not is_subpath(fp):
        raise Exception("Attempting to save file outside of project root.")
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w") as file_obj:
        json.dump(data, file_obj)
    return


def string_to_int(s: str) -> int():
    """
    Returns an int from the given string. Commas and white spaces are removed

    Args:
        s (str): string to be converted. May include spaces, and commas

    Returns:
        int: integer conversion of given string
    """
    return int(s.replace(' ', '').replace(',', ''))
