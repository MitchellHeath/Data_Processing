import pandas as pd


def dataframe_to_csv(data):
    success = False
    while not success:
        file_path = input(f"<dataframe_to_csv>\nEnter the filepath for the new file your data will go into.\n")
        try:
            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False)
            print(f'***SUCCESS: File created from dataframe***\n')
            success = True
        except Exception as e:
            print(f"***ERROR: {e}***\n")
            exit_process_check()


def list_to_csv(data):
    success = False
    while not success:
        directory = input(f"<list_to_csv>\nEnter the filepath for the new file your data will go into.\n")
        try:
            df = pd.DataFrame.from_dict(data)
            df.to_csv(directory, index=False, header=False)
            print(f"***SUCCESS: File created from list***\n")
            success = True
        except Exception as e:
            print(f'***ERROR: {e}***\n')
            exit_process_check()


def exit_process_check():
    exit_process_confirmation = input(f"Do you want to EXIT this process? (y/n)\n")
    if exit_process_confirmation == 'y':
        quit()
