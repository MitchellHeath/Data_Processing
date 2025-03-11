import Internal_Libraries.csv_to_dataset as cd
import Internal_Libraries.dataset_to_csv as dc
import datetime as t


def find_unique_values():
    unique_vals = []
    records_sorted = 0
    for v in list_w_dupes:
        records_sorted += 1
        if v not in unique_vals:
            unique_vals.append(v)
        if records_sorted % 100000 == 0:
            print(f"\nCurrent Time: {t.datetime.now()} | Start Time: {start_time}")
            print(f"{unique_vals:,} unique values found.")
            print(f"{records_sorted:,} records sorted of {list_w_dupes_length} records found")
    return unique_vals, records_sorted


start_time = t.datetime.now()
print(f"{start_time} process start.")
list_w_dupes = cd.csv_multiple_column_to_list()
list_w_dupes_length = f'{len(list_w_dupes):,}'
print(f"{list_w_dupes_length} records found")

unique_vals_returned, records_sorted_returned = find_unique_values()

print("\nPROCESSED FINISHED")
print(f"Current Time: {t.datetime.now()} | Start Time: {start_time}")
print(f"{len(unique_vals_returned):,} unique values found.")
print(f"{records_sorted_returned:,} records sorted of {list_w_dupes_length} records found\n\n")

dc.list_to_csv(unique_vals_returned)
