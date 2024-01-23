import tabulate
import requests
def everything(user_query,search_in,from_date=None,to_date=None,pageSize=None):
    url= f'https://newsapi.org/v2/everything?q={user_query}&apiKey=20a0c464f00841a2b4019d426e96948a'
    if search_in is not None:
        url=f'https://newsapi.org/v2/everything?q={user_query}&apiKey=20a0c464f00841a2b4019d426e96948a&{search_in}'
    if from_date is not None and to_date is not None:
        url=url+f'&from={from_date}&to={to_date}'
    if pageSize is not None:
        url=url+f'&pageSize={pageSize}'
    r=requests.get(url)
    if r.status_code==200:
        output=r.json()
        if len(output['articles'])>0:
            outer_list=[]
            for ele in output['articles']:
                inner_list=[ele['author'],ele['title'],ele['publishedAt']]
                outer_list.append(inner_list)
            print(tabulate.tabulate(outer_list,headers=['Author Name','Title','Publish Date'],tablefmt='simple_grid'))
        else:print(f'No results found with query:{user_query}')
    else:print(f'Error while getting the data : reason={r.reason} : {r.status_code}')
def top_headlines(country_code,user_category=None,pagesize=None):
    url=f'https://newsapi.org/v2/top-headlines?country={country_code}&apiKey=20a0c464f00841a2b4019d426e96948a'
    if user_category is not None:
        url=url+f'&category={user_category}'
    if pagesize is not None:
        url=url+f'&pageSize={pagesize}'
    r = requests.get(url)
    if r.status_code == 200:
        output = r.json()
        if len(output['articles']) > 0:
            outer_list = []
            for ele in output['articles']:
                inner_list = [ele['author'], ele['title'], ele['publishedAt']]
                outer_list.append(inner_list)
            print(tabulate.tabulate(outer_list, headers=['Author Name', 'Title', 'Publish Date'], tablefmt='simple_grid'))
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
            search_in = {'1': None, '2': 'title', '3': 'description', '4': 'content'}
            print('1,All fields', '2.search in title', '3.search in Description', '4.search in content')
            search_in = search_in[input('Enter your choice: ')]
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
            choice = {'1': 'ae', '2': 'ar', '3': 'at', '4': 'au', '5': 'be', '6': 'bg', '7': 'br', '8': 'ca', '9': 'ch',
                      '10': 'cn', '11': 'co', '12': 'cu', '13': 'cz', '14': 'de', '15': 'eg', '16': 'fr', '17': 'gb',
                      '18': 'gr', '19': 'hk', '20': 'hu', '21': 'id', '22': 'ie', '23': 'il', '24': 'in', '25': 'it',
                      '26': 'jp', '27': 'kr', '28': 'lt', '29': 'lv', '30': 'ma', '31': 'mx', '32': 'my', '33': 'ng',
                      '34': 'nl', '35': 'no', '36': 'nz', '37': 'ph', '38': 'pl', '39': 'pt', '40': 'ro', '41': 'rs',
                      '42': 'ru', '43': 'sa', '44': 'se', '45': 'sg', '46': 'si', '47': 'sk', '48': 'th', '49': 'tr',
                      '50': 'tw', '51': 'ua', '52': 'us', '53': 've', '54': 'za'}
            print('1.United Arab Emirates', '2.Argentina', '3.Austria', '4.Australia', '5.Belgium', '6.Bangladesh',
                  '7.Brazil', '8.Canada', '9.China', '10.Comoros', '11.Colombia', '12.Cuba', '13.Czech Republic',
                  '14.Germany', '15.Egypt', '16.France', '17.Gabon', '18.Greece', '19.Hong Kong', '20.Hungary',
                  '21.Indonesia', '22.Ireland', '23.Israel', '24.India', '25.Italy', '26.Japan', '27.Kiribati',
                  '28.Lithuania', '29.Latvia', '30.Madagascar', '31.Mexico', '32.Malaysia', '33.Nigeria',
                  '34.Netherlands', '35.Norway', '36.New Zealand', '37.Philippines', '38.Poland', '39.Portugal',
                  '40.Romania', '41.Serbia', '42.Russia', '43.Saudi Arabia', '44.Seychelles', '45.Singapore',
                  '46.Slovenia', '47.Slovakia', '48.Thailand', '49.Turkey', '50.Taiwan', '51.Ukraine',
                  '52.United States', '53.Venezuela', '54.Zambia', sep='\n')
            country_code = choice[input('Enter your choice: ')]
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








