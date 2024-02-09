import requests, os,csv
from tabulate import tabulate
from configparser import ConfigParser
from datetime import datetime
from yaml import safe_load
def config_file(section,option,mode):
    if mode=='ini':
        file=ConfigParser()
        file.read('config.ini')
        return file.get(section,option)
    elif mode=='yml':
        file = open('config.yml','r')
        data = safe_load(file)
        file.close()
        return data[section][option]


def choice_decision(start,stop):
    while True:
        decision=input('Enter your choice: ')
        if int(decision) in range(start,stop):
            return decision
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
    print('select the category to search based on','1.search in Titles','2.search in Description','3.search in Content','4.search in all Fileds',sep='\n')
    based_on=config_file('everything_search',choice_decision(1,5),mode)
    if based_on != 'None':
        params['searchIn']=based_on
    if user_data('date range') is True:
        params['from']=date_validation('Start')
        params['to']=date_validation('End')
    print('sort the articles based on ','1.Relevancy','2.Popularity','3.publishedAt',sep='\n')
    if user_data('sort by') is True:
        params['sortBy']=config_file('everything_sort',choice_decision(1,4),mode)
    if user_data('page Size') is True:
        params['pageSize']= num_input('page size')
    output=call_api(url,params)
    if output is not None:
        if len(output['articles'])>0:
            outer_list=[]
            for ele in output['articles']:
                inner_list=[ele['author'],ele['title'],ele['publishedAt']]
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
    print('1.United Arab Emirates', '2.Argentina', '3.Austria', '4.Australia', '5.Belgium', '6.Bangladesh',
          '7.Brazil', '8.Canada', '9.China', '10.Comoros', '11.Colombia', '12.Cuba', '13.Czech Republic',
          '14.Germany', '15.Egypt', '16.France', '17.Gabon', '18.Greece', '19.Hong Kong', '20.Hungary',
          '21.Indonesia', '22.Ireland', '23.Israel', '24.India', '25.Italy', '26.Japan', '27.Kiribati',
          '28.Lithuania', '29.Latvia', '30.Madagascar', '31.Mexico', '32.Malaysia', '33.Nigeria',
          '34.Netherlands', '35.Norway', '36.New Zealand', '37.Philippines', '38.Poland', '39.Portugal',
          '40.Romania', '41.Serbia', '42.Russia', '43.Saudi Arabia', '44.Seychelles', '45.Singapore',
          '46.Slovenia', '47.Slovakia', '48.Thailand', '49.Turkey', '50.Taiwan', '51.Ukraine',
          '52.United States', '53.Venezuela', '54.Zambia', sep='\n')
    country=config_file('headlines_country',choice_decision(1,55),mode)
    params['country']=country
    if user_data('perticuler category') is True:
        print('1.Business', '2.Entertainment', '3.General', '4.Health', '5.Science', '6.Sports',
          '7.Technology', sep='\n')
        params['category']=config_file('headlines_category',choice_decision(1,8),mode)
    if user_data('page Size') is True:
        params['pageSize']=num_input('page size')
    output=call_api(url,params)
    if output is not None:
        if len(output)>0:
            outer_list=[]
            for ele in output['articles']:
                inner_list=[ele['author'],ele['title'],ele['publishedAt']]
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
        print('Please select where would you like to see the results','1.output console','2.text file','3.csv file',sep='\n')
        output_decision=choice_decision(1,4)
        if output_decision=='1':type='console'
        elif output_decision=='2': type='txt'
        elif output_decision=='3':type='csv'
        print('please select your search choice','1.Everything API','2.Top Headlines API',sep='\n')
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