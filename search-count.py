import csv
import pandas as pd

from pandas import *


# Process uses a pre-determined list of keywords and checks the number of times those words appear in a data set
def get_filepath(first_path: bool):
    if first_path:
        print("Do you want to use the same directory used for the dataset? (yes/no)")
        use_new_directory = input()
        if use_new_directory == "yes":
            filepath = csvpath_to_list
            print("\nEnter the filename of the csv (Exclude .csv)")
            filename = input()
        else:
            print(r"Enter filepath for your csv")
            filepath = input()

            print("\nEnter the filename of the csv (Exclude .csv)")
            filename = input()
    return rf"{filepath}\{filename}.csv"


def csv_to_list(directory, header):
    data = read_csv(directory)
    list_fromCsv = data[header].tolist()
    return list_fromCsv


def csv_to_dict(directory):
    dict = []
    with open(directory, "r") as data:
        for row in csv.DictReader(data):
            dict.append(row)
    return dict


def list_to_csv(list, directory):
    df = pd.DataFrame.from_dict(list)
    df.to_csv(directory, index=False, header=False)


def list_split(list):
    split_keyword = []
    list_keyword = []
    replace_keyword = csv_to_dict(replace_keyword_directory)
    remove_symbols = csv_to_list(remove_symbols_directory, "SYMBOL")
    not_keyword = csv_to_list(remove_keyword_directory, "Remove")
    dict_double_word = csv_to_dict(double_worder_directory)
    for i in list:  # first split the sentence in each row into separate strings
        try:
            split_keyword.append(i.split())
        except:
            continue
    for i_sk in split_keyword:  # second append the strings into a single list
        for j_sk in i_sk:
            for keys_rk in replace_keyword:
                try:
                    j_sk = j_sk.replace(keys_rk["ORIGINAL"], keys_rk["NEW"])
                except:
                    continue
            double_worder = False
            if (
                    j_sk.lower() not in not_keyword
            ):  # exclude inconsequential strings for data cleanup
                for i_rs in remove_symbols:
                    try:
                        j_sk = j_sk.replace(i_rs, "")
                    except:
                        continue
                for key_dw in dict_double_word:
                    try:
                        if (j_sk + " " + i_sk[i_sk.index(j_sk) + 1]).lower() == key_dw[
                            "DOUBLE"
                        ].lower():
                            list_keyword.append(key_dw["DOUBLE"])
                            double_worder = True
                    except:
                        pass
                    try:
                        if (i_sk[i_sk.index(j_sk) - 1] + " " + j_sk).lower() == key_dw[
                            "DOUBLE"
                        ].lower():
                            continue
                    except:
                        pass
                    try:
                        if (i_sk[i_sk.index(j_sk) - 1] + " " + j_sk).lower() != key_dw[
                            "DOUBLE"
                        ].lower() and j_sk.lower() == key_dw.lower():
                            list_keyword.append(key_dw["DOUBLE"])
                            double_worder == True
                            continue
                    except:
                        pass
                if j_sk in key_dw["DOUBLE"]:
                    continue
                elif double_worder != True:
                    list_keyword.append(j_sk)
    return list_keyword


def keyword_match_to_original_list(keyword_list, original_list):
    keyword_list_deduped = [*set(keyword_list)]
    for k in keyword_list_deduped:
        for o in original_list:
            if k in o:
                print(f'Yes -> "{k}" in "{o}"')
            else:
                print(f'No  -> "{k}" in "{o}"')
    return "tbd"


print(r"Enter filepath for your csv data source")
csvpath_to_list = input()

print("\nEnter the filename of the csv (Exclude .csv)")
csvfile_to_list = input()
csv_directory = rf"{csvpath_to_list}\{csvfile_to_list}.csv"

print("\nEnter the header name of the list in the csv file")
header_name = input()
print()  # New line since \n will not work in the next print()

print(r"Enter filepath for the new csv file")
csv_new_path = input()
print("\nEnter the filename of the new csv (Exclude .csv)")
csv_new_name = input()

# Fix misspelled words or replace with a word you want to use. Ex: "MS" -> "Microsoft" or "Corona" -> "Covid19"
replace_keyword_directory = (
    r"C:\Users\mitheath\OneDrive - Cisco\Data\SupportFiles\list_keyword replace.csv"
)
# Remove words that clutter the dataset. Ex: "1234", "abcd123"
remove_keyword_directory = (
    r"C:\Users\mitheath\OneDrive - Cisco\Data\SupportFiles\list_keywords removed.csv"
)
# Takes into account that there are compound words with spaces
double_worder_directory = (
    r"C:\Users\mitheath\OneDrive - Cisco\Data\SupportFiles\dict_double worder.csv"
)
# Removes special characters
remove_symbols_directory = (
    r"C:\Users\mitheath\OneDrive - Cisco\Data\SupportFiles\list_symbols removed.csv"
)

list_original = csv_to_list(csv_directory, header_name)
list_cleaned = list_split(list_original)
csv_new_directory = rf"{csv_new_path}\{csv_new_name}.csv"
list_to_csv(list_cleaned, csv_new_directory)

print(f"{list_cleaned}\n\n")
# keyword_match_to_original_list(list_cleaned, list_original)
