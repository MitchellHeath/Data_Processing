import os
import pandas as pd
from Internal_Libraries import dataset_to_csv as dc
from Internal_Libraries import csv_to_dataset as cd


def dataset_stack_method():
    new_column_name = ""
    new_column_values_replace_yn = ""
    dataset_stack = []
    print("\n<dataset_stack>")

    print("Enter the filepath for the directory list.\n***This will collect ALL files from the folder. The "
          "folder also CANNOT contain additional folders.")
    file_list_directory = input()
    success_csv_upload = False
    while not success_csv_upload:
        try:
            file_list = os.listdir(file_list_directory)
            print('\n***SUCCESS: Data upload***')
            success_csv_upload = True
        except Exception as e:
            print(f'\n{e}\nPlease try again...')

    print("\nDo you need to add a column that distinguishes stacked datasets? (y/n)")
    new_column_yn = input()
    if new_column_yn == "y":
        print("\nWhat is the name of the new column? (no spaces; use underscore '_')")
        new_column_name = input()

        print("\nIs there a consistent string that needs to be removed/replaced from the new column values? (y/n)")
        new_column_values_replace_yn = input()
        if new_column_values_replace_yn == "y":
            print("\nEnter the string that needs to be replaced.")
            new_column_values_replace_string = input()
            print("Enter the replacement for the string. If there is no replacement and you just want to delete the "
                  "original string, simply press ENTER without input.")
            new_column_values_replace_string_replacement = input()

    for f in file_list:
        filename = rf"{file_list_directory}\{f}"
        file_dataframe = pd.read_csv(filename)
        # TODO: Add logic that will make adding a new column more flexible for other scenarios
        # Does the user want to add a column(s)? How is the column name determined? How is the column data
        # determined?, etc
        if new_column_values_replace_yn == "y":
            print("\nEnter the string that needs to be replaced.")
            new_column_values_replace_string = input()
            print("Enter the replacement for the string. If there is no replacement and you just want to delete "
                  "the original string, simply press ENTER without input.")
            new_column_values_replace_string_replacement = input()
            success_new_column = False
            while not success_new_column:
                try:
                    file_dataframe[new_column_name] = f.replace(new_column_values_replace_string,
                                                                new_column_values_replace_string_replacement)
                    success_new_column = True
                except Exception as e:
                    print(f'\n***ERROR: {e}***')
                    print(f"\nNew column {new_column_name} | {f} : {new_column_values_replace_string} does "
                          f"not exist and cannot be replaced.")
                    input('Please try again...')
        dataset_stack.append(file_dataframe)
    dataset_stack = pd.concat(dataset_stack)

    dc.dataframe_to_csv(dataset_stack)

    print("\n***PROCESS COMPLETE: dataset_stack.py***")
