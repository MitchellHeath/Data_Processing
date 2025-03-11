from Internal_Libraries import csv_to_dataset as cd
from Internal_Libraries import dataset_to_csv as dc
from Internal_Libraries import dataset_stack as ds

print("\nIs your data source spread out over multiple files? (y/n)\nNOTE: The files MUST be in a single folder if there are "
      "more than one.")
success_multiple_files = False
while not success_multiple_files:
    data_in_multiple_files = input()
    try:
        if data_in_multiple_files == "y":
            ds.dataset_stack_method()
            success_multiple_files = True
        elif data_in_multiple_files == "n":
            success_multiple_files = True
    except Exception as e:
        print(f"***ERROR: {e}***")
        print("Input must be either 'y' or 'n'.")

print("\n-Loading file data for analysis-")
dataframeRaw = cd.csv_to_dataframe()
print("\n-The data you have uploaded needs to be filtered to a smaller list of sites. The next step will help you "
      "select the file with the sites you need. Be ready with the column name from this file that has the sites. If "
      "the file does not have a column name, add one now then save and close the file.-")
dataframe_filter = cd.csv_multiple_column_to_list()

success_dataframeFiltered = False
while not success_dataframeFiltered:
    print('\nEnter the column name in the dataframe with the site names that you need to filter.')
    column_filter_name = input()
    try:
        dataframe_filtered = dataframeRaw[dataframeRaw[column_filter_name].isin(dataframe_filter)]
        success_dataframeFiltered = True
    except Exception as e:
        print(f"***ERROR: {e}***")

print("\n>Preparing to SUM grouped by Feature and Site...")
print("Enter the name of the column you want to get the SUM.")  # Action, User, Meeting
column_sum = input()
print()  # Adds a break to the next line added by

success_calculation1 = False
while not success_calculation1:
    try:
        resultsSum_FeatureUse_byFeatureSite = (
            dataframe_filtered.groupby(['featureName', 'actionName', 'appName', 'siteName'])[column_sum].sum()
            .reset_index())
        dc.dataframe_to_csv(resultsSum_FeatureUse_byFeatureSite)
        success_calculation1 = True
    except Exception as e:
        print(f'***ERROR: {e}***')
        print(f"\nRe-enter the column name")
        column_sum = input()

# print("\n>Preparing to SUM grouped by Feature, Site, and uaType...")
# success_calculation2 = False
# while not success_calculation2:
#     try:
#         resultsSum_FeatureUse_byuaType = (
#             dataframe_filtered.groupby(['featureName', 'actionName', 'appName',  'siteName'])[column_sum]
#             .sum().reset_index())
#         dc.dataframe_to_csv(resultsSum_FeatureUse_byuaType)
#         success_calculation2 = True
#     except Exception as e:
#         print(f'***ERROR: {e}***')
#         print(f"\nRe-enter the column name")
#         column_sum = input()

print("\n>Preparing to SUM grouped by Feature, Site, and WeekNum")
success_calculation3 = False
while not success_calculation3:
    try:
        resultsSum_FeatureUse_byweekNum = (
            dataframe_filtered.groupby(['featureName', 'actionName', 'appName',  'siteName', 'yearWeekNum',
                                        'yearCalendar'])[column_sum].sum()
            .reset_index())
        dc.dataframe_to_csv(resultsSum_FeatureUse_byweekNum)
        success_calculation3 = True
    except Exception as e:
        print(f"***ERROR: {e}***")
        print(f"\nRe-enter the column name")
        column_sum = input()

print("\n***PROCESS COMPLETE: feature_analysis.py***\n\n")
