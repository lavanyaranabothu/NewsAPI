from configparser import ConfigParser
from datetime import datetime
from tabulate import tabulate
from yaml import safe_load
import requests, os, csv

def get_config(section, option, mode):
    if mode == 'ini':
        config = ConfigParser()
        config.read("config.ini")
        return config.get(section, option)
    elif mode == 'yml':
        f = open('config.yaml', 'r', encoding='utf-8')
        config_data = safe_load(f)
        f.close()
        return config_data[section][option]


def output_format(type, data, headings):
    if type == 'con':
        print(tabulate(data, headers=headings, tablefmt='grid'))
    elif type == 'txt':
        filepath = f'{datetime.now().strftime("Output_%Y_%m_%d")}.txt'
        if os.path.exists(filepath):  file_mode = 'a'
        else: file_mode = 'w'
        file = open(filepath, file_mode)
        file.write(tabulate(data, headers=headings, tablefmt='grid'))
        file.close()
        if file_mode == 'w': print(f'{filepath} File Created Successfully..!')
        if file_mode == 'a': print(f'{filepath} File Updated Successfully..!')
    elif type == 'csv':
        filepath = f'{datetime.now().strftime("Output_%Y_%m_%d")}.csv'
        file = open(filepath, "w")
        csv_write = csv.writer(file)
        csv_write.writerow(headings)
        print(f'{filepath} File Created Successfully..!')

def take_user_decision(start, stop):
    while True:
        choice = input('Enter your choice : ')
        if int(choice) in range(start, stop): return choice
        else: print(f'Invalid Selection, You have to select in the range of {start} and {stop}')

def capture_decision(purpose):
    while True:
        decision = input(f'Do you want to enter {purpose} (y/n) : ')
        if decision in ['y', 'Y']: return True
        elif decision in ['n', 'N']: return False
        else: print("Invalid selection. select either Y/N")

def validate_date(purpose):
    date = input(f'Enter {purpose} Date (YYYY-MM_DD) : ')
    datetime.strptime(date, '%Y-%m-%d')
    return date

def validate_number(purpose):
    while True:
        num = input(f'Enter {purpose} : ')
        if num.isdigit(): return int(num)
        else: print('Enter only digits not alphabets or special characters')

def perform_api_call(url, params=None):
    response = requests.get(url, params)
    if response.status_code == 200:
        print('Hurray..! We got results from server')
        return response.json()
    else:
        print(f'Error while making API Call | Status Code : {response.status_code} | Reason : {response.reason}')

def everything_endpoint(mode, fmt):
    print('You have selected Everything Endpoint')
    url = f"{get_config('basic', 'base_url', mode)}{get_config('basic', 'everything_url', mode)}"
    search_query = input('Enter Your Query : ')
    params = {'apikey': get_config('basic', 'apikey', mode), 'q': search_query}
    print('Select Search query based on', '1. Title', '2. Description', '3. Content', '4. All Fields', sep='\n')
    based_on = get_config('everything_search', take_user_decision(1, 5), mode)
    if based_on != 'None': params['searchIn'] = based_on
    if capture_decision('dates') is True:
        params['from'] = validate_date('Start')
        params['to'] = validate_date('End')
    if capture_decision('Sorting Selection') is True:
        print('Select Sorting Type', '1. Relevancy', '2. Popularity', '3. Published Date', sep='\n')
        sortby = get_config('everything_sort', take_user_decision(1, 4), mode)
        params['sortBy'] = sortby
    if capture_decision('Page Size') is True:
        params['pageSize'] = validate_number('Page Size')
    output = perform_api_call(url, params)
    if output is not None:
        if len(output['articles']) > 0:
            outer_list = []
            for record in output['articles']:
                outer_list.append([record['author'], record['title'], record['publishedAt']])
            if mode == 'ini': headings = get_config('headings', 'everything', mode).split(',')
            elif mode == 'yml': headings = get_config('headings', 'everything', mode)
            output_format(type=fmt, data=outer_list, headings=headings)
        else:
            print(f'There are no results for your search : {search_query}')


def topheadlines_endpiont(mode, fmt):
    print('You have selected Everything Endpoint')
    url = f"{get_config('basic', 'base_url', mode)}{get_config('basic', 'topheadlines_url', mode)}"
    params = {'apikey': get_config('basic', 'apikey', mode)}
    print('1.United Arab Emirates', '2.Argentina', '3.Austria', '4.Australia', '5.Belgium', '6.Bulgaria',
          '7.Brazil',
          '8.Canada', '9.Switzerland', '10.People’s Republic of China', '11.Colombia', '12.Cuba',
          '13.Czech Republic',
          '14.Germany', '15.Egypt', '16.France', '17.United Kingdom (no new registrations, see also UK)',
          '18.Greece',
          '19.Hong Kong', '20.Hungary', '21.Indonesia', '22.Ireland', '23.Israel', '24.India', '25.Italy',
          '26.Japan',
          '27.Korea, Republic Of', '28.Lithuania', '29.Latvia', '30.Morocco', '31.Mexico', '32.Malaysia',
          '33.Nigeria', '34.Netherlands',
          '35.Norway', '36.New Zealand', '37.Philippines, Republic of the', '38.Poland', '39.Portugal',
          '40.Romania', '41.Serbia',
          '42.Russian Federation', '43.Saudi Arabia', '44.Sweden', '45.Singapore', '46.Slovenia',
          '47.Slovakia (Slovak Republic)',
          '48.Thailand', '49.Turkey', '50.Taiwan', '51.Ukraine', '52.United States', '53.Venezuela',
          '54.South Africa', sep="\n")
    countrydict= get_config('country_search', take_user_decision(1, 55), mode)
    if countrydict!=None: params['country']=countrydict
    if capture_decision('category Selection') is True:
        print('Select Category Type', '1. business', '2. entertainment', '3. general', '4. health','5. science','6. sports','7. technology',sep='\n')
        sortby = get_config('category sort', take_user_decision(1, 8), mode)
        params['category'] = sortby
    if capture_decision('Page Size') is True:
        params['pageSize'] = validate_number('Page Size')
    output = perform_api_call(url, params)
    if output is not None:
        if len(output['articles']) > 0:
            outer_list = []
            for record in output['articles']:
                outer_list.append([record['author'], record['title'], record['publishedAt']])
            if mode == 'ini': headings = get_config('headings', 'everything', mode).split(',')
            elif mode == 'yml': headings = get_config('headings', 'everything', mode)
            output_format(type=fmt, data=outer_list, headings=headings)
        else:
            print(f'There are no results for your search')




def main():
    print('Welcome to the News Channel')

    print('Select Config File', '1. INI file', '2. YAML file', '3. JSON file', sep='\n')
    config_selection = take_user_decision(1, 4)
    if config_selection == '1': mode = 'ini'
    elif config_selection == '2': mode = 'yml'
    elif config_selection == '3': mode = 'json'

    print('Select Data output format', '1. Console', '2. Text File', '3. CSV File', sep='\n')
    output_selection = take_user_decision(1, 4)
    if output_selection == '1': fmt = 'con'
    elif output_selection == '2': fmt = 'txt'
    elif output_selection == '3': fmt = 'csv'

    print('Select Your Preference', '1. Search Everything', '2. Top Headlines', sep='\n')
    choice = take_user_decision(1, 3)
    if choice == '1': everything_endpoint(mode, fmt)
    elif choice == '2': topheadlines_endpiont(mode, fmt)

main()