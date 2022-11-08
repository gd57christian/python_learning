# standard library imports
import os
import sqlite3

# todo get rid of the default value

def check_file_type(file_path, file_type="png"):
    """
    Returns:
        True or False, after check the file type
    Args:
        file_path: list of path from the founded files
        file_type: string with extension of the file
    """
    head , extension = os.path.splitext(file_path)
    if extension:
        extension = extension[1:].lower()
        if extension == file_type:
            return True
        else:
            return False
    else:
        return False

def search_file_type(root_path, file_type='png'):
    """
    check the file type and return True or False
    Args:
        root_path: base root path
        file_type: string with extension of the file
    """
    list_file_type = []

    for root, dirs, files in os.walk(root_path):
        for file in files:
            if check_file_type(file, file_type):
                list_file_type.append(os.path.join(root, file))

    return list_file_type

def add_database(database_path, filelist, filetype):
    """
    creating/adding data tothe database file
    Args:
        database_path: file path
        filelist: data list
        filetype: extension of the file
    """
    connect = sqlite3.connect(database_path)
    cursor =  connect.cursor()

    # creating variable to check if the database file already exist
    var = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='files_found'")
    var = var.fetchone()
    # create database if not exist
    if not var:
        cursor.execute("""CREATE TABLE files_found (file_type TEXT,
                                                  file_path TEXT)""")
    # adding values to the database
    main_list = [(filetype, item) for item in filelist]
    cursor.executemany("INSERT INTO files_found(file_type, file_path) VALUES (?, ?)", main_list)

    # commit and close the database
    connect.commit()
    connect.close()