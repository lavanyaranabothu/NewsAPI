import requests
import tabulate

def everthing(userchoice,basedon,from_date=None,to_date=None,records=None):
    url = f'https://newsapi.org/v2/everything?q={userchoice}&apiKey=d66a2c5691fe4db1826283f00030b28e'
    if basedon is not None:
        url = url + f'&searchIn = {basedon}'
    elif from_date is not None and to_date is not None:
        url = url + f'&from_date = {from_date} & to_date = {to_date}'
    elif records is not None:
        url = url + f'&pageSize = {records}'

    print(url)
# response = requests.get(f'https://newsapi.org/v2/everything?q={userchoice}&apiKey=d66a2c5691fe4db1826283f00030b28e')
# if response.status_code == 200:
#         output = response.json()
#         outer_list = []
#         for ele in output['articles']:
#             inner_list = (ele['source']['id'],ele['source']['name'], ele['author'],ele['title'],ele['description'],ele['publishedAt'],ele['content'])
#             outer_list.append(inner_list)
#         print(tabulate.tabulate(outer_list,headers =('id','name','author','title','description','publishedAt','content'),tablefmt='simple_grid'))
# else:
#     print('invalid data')

def top_headlines(country,category,records=None):
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey=d66a2c5691fe4db1826283f00030b28e'
    if country is not None:
        url = url + f'&countries = {country}'
    elif category is not None:
        url = url + f'&category = {category}'
    elif records is not None:
        url = url + f'&pageSize= {records}'

    print(url)

def main():
    print(" welcome to NEWS API :  ")
    while True:
        print("1.everthing api","2.headlines api",sep='\n')
        choice=input(" enter user choice :")
        if choice=="1":
            userchoice = input(" Enter the choice  : ")
            searchdict = {"1": None, "2": "Title", '3': "Description", "4": "Content"}
            print("1.Search in All Fields", "2.Search in Title", "3.search in Description", "4.search in content",
                  sep='\n')
            choice = input(" Enter Search Details :")
            basedon = searchdict[choice]
            fromdate,todate = None, None
            while True:
                Date = input("Do you wish to continue with Date (y/n) : ")
                if Date in ["Y", "y"]:
                    fromdate = input(" Enter From date (yyyy-mm-dd) :")
                    todate = input("Enter To date (yyyy-mm-dd)      : ")
                    break
                elif Date in ["N", "n"]:
                    break
                else:
                    print(" Enter either yes or no ")
            Records=None
            while True:
                record = input(" Do you wish to limit the pagecount (y/n) :")
                if record in ["Y", "y"]:
                    Records=input(" enter the page count : ")
                    break
                elif record in ["N", "n"]:
                    break
                else:
                    print(" select either yes or no ")

            everthing(userchoice,basedon,from_date=None,to_date=None,records=None)

        if choice == '2':
            userchoice = input('Enter the choice : ')
            search_dic = {'1': 'UAE', '2': 'AUS ','3': 'BEL', '4': 'BGR','5': 'BR',
                          '6': 'CA','7': 'CHE','8': 'CHN','9': 'COL','10': 'CUB','11': 'CZ','12': 'DEU',
                          '13': 'EG','14': 'FR','15': 'GB', '16': 'GR','17': 'HK','18': 'HU','19': 'ID',
                          '20': 'IE','21': 'IL','22': 'IN','23': 'IT','24': 'JP', '25': 'KR','26': 'LT',
                          '27': 'LV','28': 'MA','29': 'MX','30': 'MY','31': 'NG','32': 'NL','33': 'NO',
                          '34': 'NZ','35': 'PH','36': 'PL','37': 'PT','38': 'RO','39': 'RS','40': 'RU',
                          '41': 'SA','42': 'SE','43': 'SG','44': 'SI','45': 'SK','46': 'TH','47': 'TR',
                          '48': 'TW','49': 'UA','50': 'USA','51': 'VE','52': 'ZA','53': 'AR','54': 'AT'}
            print('1. United Arab Emirates', '2. Australia', '3. Belgium', '4. Bulgaria','5. Brazil',
                  '6. Canada','7. Switzerland','8. China','9. Colombia','10. Cuba','11. Czech Republic','12. Germany',
                  '13. Egypt','14. France','15. United Kingdom','16. Greece','17. Hong Kong',
                  '18. Hungary','19. Indonesia','20. Ireland','21. Israel','22. India','23. Italy','24. Japan',
                  '25. Korea','26. Lithuania','27. Latvia','28. Morocco','29. Mexico','30. Malaysia','31. Nigeria',
                  '32. Netherlands','33. Norway','34. New Zealand','35. Philippines','36. Poland','37. Portugal',
                  '38. Romania','39. Serbia', '40. Russian Federation','41. Saudi Arabia','42. Sweden','43. Singapore',
                  '44. Slovenia','45. Slovakia','46. Thailand','47. Turkey','48. Taiwan','49. Ukraine',
                  '50. United States of America','51. Venezuela','52. South Africa','53. Argentina','54. Austria',sep='\n')



# while True:
#     check_country = input('Do you wish to continue with country name (y/n):')
#     if check_country in ['Y','y']:
#         country = input('enter the country :')
#         break
#     elif check_country in ['N', 'n']:
#         break
#     else:
#         print('enter either yes or no')

            country = search_dic[userchoice]
            choice1 = input('enter the category')
            print('1. BUSINESS','2. ENTERTAINMENT', '3. GENERAL','4. HEALTH','5. SCIENCE','6. SPORTS','7. TECHNOLOGY', sep='\n')
            search_dic1= {'1': 'business','2': 'entertainment','3': 'general',
                          '4': 'health','5': 'science','6': 'sports', '7': 'technology'}

            category = search_dic1[choice1]

            while True:
                check_category = input('Do you wish to continue with category name (y/n):')
                if check_category in ['Y','y']:
                    category = input('enter the category :')
                    break
                elif check_category in ['N', 'n']:
                    break
                else:
                    print('enter either yes or no')

            top_headlines(country,category,records=None)
        else: print(" Enter Valid Option  ")
        userdecision=input(" Do you wish to continue (y/n) :")
        if userdecision in ["Y","y"]: continue
        else: break
main()

#top_headlines(country,category)