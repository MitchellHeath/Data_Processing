import Internal_Libraries.csv_to_dataset as cd
import Internal_Libraries.dataset_to_csv as dc
import pandas as pd


print('***Data cleanup should be done BEFORE running this executable (e.g. string separator should be ",", remove/edit '
      'words, etc.)***')
dataset_from_csv = cd.csv_to_dataframe()

success_columnNames = False
while not success_columnNames:
    print('\nNext, the process requires two column names. The first is the column name that you would filter in Excel '
          'to identify the information you need split. The second column name has the data that needs to be split.'
          '\n***NAMES ARE CASE-SENSITIVE***')
    print("Enter the first column name.")
    column_name1 = input()
    print("Enter the second column name.")
    column_name2 = input()
    try:
        site_df = pd.DataFrame(columns=[column_name1, column_name2])
        success_columnNames = True
    except Exception as e:
        print(f'***ERROR: {e}***\nTry again.')

for i, row in dataset_from_csv.iterrows():
    site_org = row[column_name1]
    site_string = row[column_name2]
    j = len(site_df)  # var j needs to pickup where 'for s [loop]' left off
    # noinspection PyBroadException
    try:
        for s in site_string.split(', '):
            site_df.loc[j] = [site_org, s]
            j += 1
            # print(site_org + ' | ' + s)  # todo: prod COMMENT line
    except Exception as e:
        continue

print(site_df)
dc.dataframe_to_csv(site_df)
print()
print()
