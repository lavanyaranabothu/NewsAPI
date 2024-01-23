import requests
import tabulate
from configparser import ConfigParser
def get_config(section,option):
    parser=ConfigParser()
    parser.read('config.ini')
    return parser.get(section, option)
def everything(user_query,search_in,from_date=None,to_date=None,pageSize=None):
    url= f'{get_config('everything','my_url')}'
    my_dict={'q':user_query,'apiKey':get_config('everything','apikey')}
    if search_in is not None:
        my_dict['searchIn']= search_in
    if from_date is not None and to_date is not None:
        my_dict['from']=from_date
        my_dict['to']=to_date
    if pageSize is not None:
        my_dict['pageSize']=pageSize

    r=requests.get(url,params=my_dict)
    if r.status_code==200:
        output=r.json()
        if len(output['articles'])>0:
            outer_list=[]
            for ele in output['articles']:
                inner_list=[ele['author'],ele['title'],ele['publishedAt']]
                outer_list.append(inner_list)
            print(tabulate.tabulate(outer_list,headers=[get_config('everything','everything_headers').split(',')],tablefmt='simple_grid'))
        else:print(f'No results found with query:{user_query}')
    else:print(f'Error while getting the data : reason={r.reason} : {r.status_code}')
def top_headlines(country_code,user_category=None,pagesize=None):
    url=f'{get_config('headlines','my_url')}'
    h_dict={'country':country_code,'apiKey':get_config('headlines','apikey')}
    if user_category is not None:
        h_dict['category']=user_category
    if pagesize is not None:
        h_dict['pageSize']=pagesize
    r = requests.get(url,params=h_dict)
    if r.status_code == 200:
        output = r.json()
        if len(output['articles']) > 0:
            outer_list = []
            for ele in output['articles']:
                inner_list = [ele['author'], ele['title'], ele['publishedAt']]
                outer_list.append(inner_list)
            print(tabulate.tabulate(outer_list, headers=[get_config('headlines','headlines_headers').split(',')], tablefmt='simple_grid'))
        else:
            print(f'No results found with query')
    else:
        print(f'Error while getting the data : reason={r.reason} : {r.status_code}')
def main():
    print('Welcome to News API')
    while True:
        print('1.Everyting API','2.Top Headlines API',sep='\n')
        choice=input('Select the API Type: ')
        if choice=='1':
            print('You have selected Everything API')
            user_query = input('Enter your search query: ')
            print('1,All fields', '2.search in title', '3.search in Description', '4.search in content')
            choice=input('Enter your choice: ')
            search_in = get_config('search_indict',choice )
            from_date = None
            to_date = None
            while True:
                user_decision = input('Would you like to add date range (y/n): ')
                if user_decision in ['y', 'Y']:
                    from_date = input('Enter from date yyyy-mm-dd: ')
                    to_date = input('Enter from date yyyy-mm-dd: ')
                    break
                else:
                    break
            pageSize = None
            while True:
                user_choice = input('Would you like to add pagesize (y/n): ')
                if user_choice in ['y', 'Y']:
                    pageSize = input('Enter number of pages: ')
                    break
                else:
                    break
            everything(user_query, search_in, from_date, to_date, pageSize)

        elif choice=='2':
            print('You have selected Top Headlines API')
            print('1.United Arab Emirates', '2.Argentina', '3.Austria', '4.Australia', '5.Belgium', '6.Bangladesh',
                  '7.Brazil', '8.Canada', '9.China', '10.Comoros', '11.Colombia', '12.Cuba', '13.Czech Republic',
                  '14.Germany', '15.Egypt', '16.France', '17.Gabon', '18.Greece', '19.Hong Kong', '20.Hungary',
                  '21.Indonesia', '22.Ireland', '23.Israel', '24.India', '25.Italy', '26.Japan', '27.Kiribati',
                  '28.Lithuania', '29.Latvia', '30.Madagascar', '31.Mexico', '32.Malaysia', '33.Nigeria',
                  '34.Netherlands', '35.Norway', '36.New Zealand', '37.Philippines', '38.Poland', '39.Portugal',
                  '40.Romania', '41.Serbia', '42.Russia', '43.Saudi Arabia', '44.Seychelles', '45.Singapore',
                  '46.Slovenia', '47.Slovakia', '48.Thailand', '49.Turkey', '50.Taiwan', '51.Ukraine',
                  '52.United States', '53.Venezuela', '54.Zambia', sep='\n')
            choice=input('Enter your choice: ')
            country_code = get_config('country_codes',choice)
            user_category = None
            while True:
                choice = input('would you like to search in perticuler category y/n: ')
                if choice in ['y', 'Y']:
                    my_dict = {'1': 'business', '2': 'entertainment', '3': 'general', '4': 'health', '5': 'science',
                               '6': 'sports', '7': 'technology'}
                    print('1.Business', '2.Entertainment', '3.General', '4.Health', '5.Science', '6.Sports',
                          '7.Technology', sep='\n')
                    user_category = my_dict[input('Enter the category: ')]
                    break
                else:
                    break
            pagesize = None
            while True:
                record = input(" Do you wish to limit the pagecount (y/n) :")
                if record in ["Y", "y"]:
                    pagesize = input(" enter the page count : ")
                    break
                else:
                    break
            top_headlines(country_code, user_category, pagesize)
        else:print('Invalid selection pleae select again')
        user_decision=input('Do you wnt to continue y/n: ')
        if user_decision in ['y','Y']:continue
        else:break
main()










