import pandas as pd
import datetime as t
from Internal_Libraries import csv_to_dataset as cd
from Internal_Libraries import dataset_to_csv as dc


# THE PROCESS PERFORMS A VLOOKUP WITH DATASETS TOO LARGE FOR EXCEL

print(f"\nThis process follows the data entry order of an Excel VLOOKUP formula.\n"
      f"Look-up Value: Enter the file information for the Look-up Value.\n")
match_df = cd.csv_to_dataframe()

success_lookup_match = False
while not success_lookup_match:
    try:
        lookup_source_match = input(f"Look-up Value: Enter the field name with the Look-up Value in the file you just "
                                    f"entered. NOTE: Case-sensitive.\n")
        lookup_source_df_column_index = match_df.columns.get_loc(lookup_source_match)
        success_lookup_match = True
    except Exception as e:
        print(f"***ERROR: {e}***\nPlease try again.\n")

print(f"\nArray: Next you will enter the name of the file that contains the Array.\n")
array_df = cd.csv_to_dataframe()

array_field_name = input(f"\nArray: Enter the name of the Array field. REMEMBER, case-sensitive.\n")

array_list = array_df[array_field_name].to_numpy()
for i in range(len(array_list)):
    array_list[i] = array_list[i].lower()

# Enter information for the new file that will be created.
match_field_name = input(f"\nMatched File: Enter the name of the new field indicating a match.\n")

# Array is compared to the Look-up Values as a new column w/ TRUE/FALSE results
# TODO: Add logic to add field values from the Array file
match_df_prep = pd.Series([])
match_df[match_field_name] = match_df_prep
count_tracker_match_complete = 0

# PROCESS START
start_time = t.datetime.now()
source_len = ('{:,}'.format(len(match_df)))
print("\nComparing Look-up Values to the Array...")
print(f"{start_time} process start. {source_len} records to search.")
count_tracker_records_sorted = 0
for i in range(len(match_df.index)):
    match_df.at[i, match_field_name] = 0  # Updated to 1 when a match is confirmed
    source_match_value = match_df.iat[i, lookup_source_df_column_index]
    if type(source_match_value) is str:
        source_match_value = source_match_value.lower()
    r_searched = i + 1
    if source_match_value in array_list:
        match_df.at[i, match_field_name] = 1
        count_tracker_match_complete += 1
    else:
        match_df.drop(match_df.loc[match_df.index == source_match_value].index)
    count_tracker_records_sorted += 1
    if r_searched % 10000 == 0:
        print(f"\nCurrent Time: {t.datetime.now()} | Start Time: {start_time}")
        print(f"{'{:,}'.format(r_searched)} Look-up Values searched of {source_len}.")
        print(f"{'{:,}'.format(count_tracker_match_complete)} matched records.")

print()  # Creates space in Command Window
dc.dataframe_to_csv(match_df)

print("\n***PROCESS COMPLETE***")
