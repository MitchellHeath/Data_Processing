import base64
import re
import requests

import Internal_Libraries.dataset_to_csv as dc
import Internal_Libraries.csv_to_dataset as cd
from bs4 import BeautifulSoup as bs
from xml.etree import cElementTree as et


directory = r"C:\Users\mitheath\OneDrive - Cisco\Documents\Project Docs\HaRT\WDA\Toggle Confirmation_automation"
filepath_INPUT_sitelist = directory
filename_INPUT_sitelist = 'WDA Confirmation_INPUT - site list.csv'
headername_INPUT_sitelist = 'Site name'
print("\n**ATTENTION**\n"
      "Make sure the csv with the site list follows these criteria:"
      f"\n 1) Is in '{filepath_INPUT_sitelist}'"
      f"\n 2) Uses the file name '{filename_INPUT_sitelist}'"
      f"\n 3) The column header must be labeled '{headername_INPUT_sitelist}'.")
input("\n**Press ENTER when the file is ready.**")
print("Process is running...")
try:
    site_list = cd.csv_to_list(filepath_INPUT_sitelist + "\\" + filename_INPUT_sitelist, headername_INPUT_sitelist)
    print("\nSource file found...")
except Exception as e:
    print(f"\n{e}")
    input("Press ENTER to exit.")
WDA_toggle_status_list = []
error_log = []

# TODO: see starting steps below
# 1) Open file with list of sites to check and move sites to an array/list
# 2) Loop the list until all sites are checked
print("\nCollecting toggle data for sites...")
for s in site_list:
    s_regex = re.search('(.*)(.webex.com)', s)
    site_name = s_regex.group(1)
    try:
        url = f'https://{site_name}.webex.com/{site_name}/featureconfig.php?AT=GC&TYPE=PT'
        headers_ = ({'User-Agent':
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                    (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
                    'Accept-Language': 'en-US, en;q=0.5'})
        page = requests.get(url, headers=headers_)
    except Exception as e:  # todo: Create a log file to track errors
        print(f"\n{e}")
        error_collection = {
            'site_name': site_name,
            'error_logged': e
        }
        error_log.append(error_collection)
        continue

    # DEBUGGING:
    # print(f'status code: {page.status_code}')
    # print(f'content: {page.content}')
    # print(f'text: {page.text}')

    soup = bs(page.content, "html.parser")
    lines = soup.prettify().splitlines()
    content = '\n'.join(lines[0:])

    xml_filename = f'{directory}\WDA_Toggle_Confirmation.xml'
    with open(xml_filename, 'w', encoding='utf-8') as out:
        out.write(content)

    # Organizes the data into a xml before transforming to a dataframe
    tree = et.parse(rf'{directory}\WDA_Toggle_Confirmation.xml')
    root = tree.getroot()
    xml_search = 'featurepayloads'
    EnableWDAToUnifiedClientGA = ''
    EnableWDAToUnifiedClientP2GA = ''

    print(f"...{site_name}: toggle data collection")
    for r in root.iter(xml_search):
        base64_string = r.text.replace('\n', '').strip()
        payload = base64.b64decode(base64_string)
        ga_regex = re.search('(EnableWDAToUnifiedClientGA..)(\w*)', payload.decode('utf-8'))
        EnableWDAToUnifiedClientGA = ga_regex.group(2)
        p2ga_regex = re.search('(EnableWDAToUnifiedClientP2GA..)(\w*)',payload.decode('utf-8'))
        EnableWDAToUnifiedClientP2GA = p2ga_regex.group(2)

    field_collection = {
        'site_name':                    site_name,
        'EnableWDAToUnifiedClientGA':   EnableWDAToUnifiedClientGA,
        'EnableWDAToUnifiedClientP2GA': EnableWDAToUnifiedClientP2GA
        }
    WDA_toggle_status_list.append(field_collection)
    # DEBUGGING:
    # print(WDA_toggle_status_list)

filename_WDAconfirmation = rf'{directory}\WDA Confirmation_RESULTS.csv'
filename_errorLog = rf'{directory}\ERROR LOG.csv'
try:
    dc.dataframe_to_csv(WDA_toggle_status_list, filename_WDAconfirmation)
except Exception as e:
    print(f"\n{e}")
try:
    dc.dataframe_to_csv(error_log, filename_errorLog)
except Exception as e:
    print(f"\n{e}")
    # input("Press ENTER to close.")
# print("\nProcess finished.")
# input("Press ENTER to close.")
