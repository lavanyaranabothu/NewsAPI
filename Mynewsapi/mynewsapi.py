import requests, os, csv, sys
from tabulate import tabulate
from configparser import ConfigParser, NoSectionError, NoOptionError
from datetime import datetime
from yaml import safe_load


def config_file(section,option,mode):
    if mode=='ini':
        file=ConfigParser()
        try:
            file.read('config1.ini')
        except FileNotFoundError:
            print('Configuration file is not available')
            sys.exit(1)
        else:
            try: return file.get(section, option)
            except NoSectionError:
                print(f'Please check mentioned {section}  not found in the file')
                sys.exit(1)
            except NoOptionError:
                print(f'Please check mentioned {option}  not found in the file')
                sys.exit(1)
    elif mode=='yml':
        try:
            file = open('config1.yml', 'r')
        except FileNotFoundError:
            print('Configuration file not available')
            sys.exit(1)
        else:
            data = safe_load(file)
            file.close()
            try: return data[section][option]
            except NoSectionError:
                print(f'Please check mentioned {section}  not found in the file')
                sys.exit(1)
            except NoOptionError:
                print(f'Please check mentioned {option}  not found in the file')
                sys.exit(1)
def choice_decision(start,stop):
    while True:
        decision=input('Enter your choice: ')
        try:
            if int(decision) in range(start,stop):
                return decision
        except: print('please enter only numbers')
        else:print(f'Invalid selection please enter in given range {start} to {stop-1}')
def user_data(purpose):
    while True:
        data=input(f'do you want enter {purpose} y/n: ')
        if data in ['y','Y']:return True
        elif data in ['n','N']:return False
        else:print('please select only Y/N')
def num_input(purpose):
    while True:
        num=input(f'enter {purpose}: ')
        if num.isdigit():
            return int(num)
        else:print('Please enter only numbers')


def date_validation(purpose):
    while True:
        date=input(f'Enter {purpose} date YYYY-MM-DD: ')
        try:
            datetime.strptime(date,'%Y-%m-%d')
            return date
        except:
            print('Invalid date format please enter in YYYY-MM-DD')
def my_output(type,data,headings):
    if type=='console':
        print(tabulate(data,headers=headings,tablefmt='grid'))
    elif type=='txt':
        file_path=f'{datetime.now().strftime("Output-%Y-%m-%d")}.txt'
        if os.path.exists(file_path):file_mode='a'
        else:file_mode='w'
        file=open(file_path,file_mode,encoding='utf-8')
        file.write(tabulate(data,headers=headings,tablefmt='grid'))
        file.close()
        if file_mode=='w':print('file created successfully..')
        elif file_mode=='a':print('file updated successfully...')
    elif type=='csv':
        filepath=f'{datetime.now().strftime("Output-%Y-%m-%d")}.csv'
        file=open(filepath,'w',encoding='utf-8')
        csv_file=csv.writer(file)
        csv_file.writerow(headings)
        csv_file.writerows(data)
        print(f'{filepath} created successfully...')


def call_api(url,params=None):
    output=requests.get(url,params)
    if output.status_code==200:
        print('Wow we got some results...')
        return output.json()
    else:print(f'Error while performing API call {output.reason} {output.status_code}')

def everything(mode,type):
    print('You have selected Everything API')
    url=f'{config_file('basic','my_url',mode)}{config_file('basic','everything_url',mode)}'
    params={'apiKey':config_file('basic','apikey',mode)}
    query=input('Enter your search query: ')
    params['q']=query
    print(f'{config_file('everything_print','search',mode)}')
    based_on=config_file('everything_search',choice_decision(1,5),mode)
    if based_on != 'None':
        params['searchIn']=based_on
    if user_data('date range') is True:
        params['from']=date_validation('Start')
        params['to']=date_validation('End')
    print(f'{config_file('everything_print','sort',mode)}')
    if user_data('sort by') is True:
        params['sortBy']=config_file('everything_sort',choice_decision(1,4),mode)
    if user_data('page Size') is True:
        params['pageSize']= num_input('page size')
    output=call_api(url,params)
    if output is not None:
        if output.get('articles')is not None:
            if len(output['articles'])>0:
                outer_list=[]
                for ele in output['articles']:
                    inner_list=[ele.get('author'),ele.get('title'),ele.get('publishedAt')]
                    outer_list.append(inner_list)
                if mode=='ini':headings=config_file('headings','everything_headings',mode).split(',')
                elif mode=='yml':headings=config_file('headings','everything_headings',mode)
                my_output(type=type,data=outer_list,headings=headings)
            else:
                print(f'oops... there are no results found with your query {query}')
def top_headlines(mode,type):
    print('You have selected Top Headlines API')
    url=f'{config_file('basic','my_url',mode)}{config_file('basic','headlines_url',mode)}'
    params={'apiKey':config_file('basic','apikey',mode)}
    print(f'{config_file('headlines_print','country',mode)}')
    country=config_file('headlines_country',choice_decision(1,55),mode)
    params['country']=country
    if user_data('perticuler category') is True:
        print(f'{config_file('headlines_print','category',mode)}')
        params['category']=config_file('headlines_category',choice_decision(1,8),mode)
    if user_data('page Size') is True:
        params['pageSize']=num_input('page size')
    output=call_api(url,params)
    if output is not None:
        if output.get('articles') is not None:
            if len(output['articles'])>0:
                outer_list=[]
                for ele in output['articles']:
                    inner_list=[ele.get('author'),ele.get('title'),ele.get('publishedAt')]
                    outer_list.append(inner_list)
                if mode=='ini':headings=config_file('headings','headlines_headings',mode).split(',')
                elif mode=='yml':headings=config_file('headings','headlines_headings',mode)
                my_output(type=type,data=outer_list,headings=headings)
            else:print('oops!.no results found with given query')


def main():
    print('Welcome to the news API')
    while True:
        print('Choose Config File','1.ini File','2.Yaml File',sep='\n')
        file_selection=choice_decision(1,3)
        if file_selection=='1':mode='ini'
        elif file_selection=='2':mode='yml'
        print(f'{config_file('main_print','output_selection',mode)}')
        output_decision=choice_decision(1,4)
        if output_decision=='1':type='console'
        elif output_decision=='2': type='txt'
        elif output_decision=='3':type='csv'
        print(f'{config_file('main_print','api_selection',mode)}')
        user_choice=choice_decision(1,3)
        if user_choice=='1':everything(mode,type)
        elif user_choice=='2': top_headlines(mode,type)
        user_decision=input('do you want to continue y/n: ')
        if user_decision in ['y','Y']:
            continue
        else:
            print('Thanks you for using News API Application..')
            break


main()