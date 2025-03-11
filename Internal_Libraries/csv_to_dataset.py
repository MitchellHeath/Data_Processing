import pandas as pd
from pandas import *


# Use this method when you have a file with only one column
def csv_single_column_to_list():
    success = False
    while not success:
        print('<csv_single_column_to_list>')
        file_path, field_name = get_file_info()
        try:
            data = read_csv(file_path)
            from_csv_list = data[field_name].tolist()
            print(f'***SUCCESS: List created from file***\n')
            success = True
            return from_csv_list
        except Exception as e:
            print(f'***ERROR: {e}***\n')
            exit_process_check()


# Use this method when you need a single column for a list from a file with
# multiple columns
def csv_multiple_column_to_list():
    success = False
    while not success:
        print('<csv_multiple_column_to_list>')
        file_path, field_name = get_file_info()
        try:
            file_contents = read_csv(file_path)
            list_contents = file_contents[field_name].tolist()
            print(f'***SUCCESS: List created from file***\n')
            success = True
            return list_contents
        except Exception as e:
            print(f'***ERROR: {e}***\n')
            exit_process_check()


# Download the full contents of the file to a dataframe
def csv_to_dataframe():
    success = False
    while not success:
        print('<csv_to_dataframe>')
        file_path, column_na = get_file_info()
        try:
            csv_data = read_csv(file_path)
            from_csv_dataframe = pd.DataFrame.from_dict(csv_data)
            print(f"***SUCCESS: Dataframe created from file***\n")
            success = True
            return from_csv_dataframe
        except Exception as e:
            print(f'***ERROR: {e}***\n')
            exit_process_check()


def get_file_info():
    file_path = input(f'Enter the filepath of your data source.\n')
    header_name = input(f'\nEnter the field name if you are generating a new list with the data. If not, because you '
                        f'are generating a dataframe, press ENTER.\n')
    return file_path, header_name


def exit_process_check():
    exit_process_confirmation = input(f"Do you want to EXIT this process? (y/n)\n")
    print()  # Empty line created between input() and the commands that follow
    if exit_process_confirmation == 'y':
        quit()
