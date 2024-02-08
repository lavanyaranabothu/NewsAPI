import requests
import tabulate
from configparser import ConfigParser
def get_config(section,option):
    parser=ConfigParser()
    parser.read("config.ini")
    return parser.get(section,option)
def everything(user_choice,basedon,Fromdate=None,Todate=None,Records=None):
    url=f'{get_config(section="everything",option="url")}'
    dict={'q': user_choice,'apiKey':get_config('everything','apikey')}
    if basedon is not None:
        dict['searchIn']=basedon
    if Fromdate is not None and Todate is not None:
        dict['from']=Fromdate
        dict['to']=Todate
    if Records is not None:
        dict['pageSize']= Records
    #print(dict)
    response=requests.get(url,params=dict)
    print(response.request.url)

def headlines(country,category,records=None):
    myurl=f'{get_config(section="headlines",option="myurl")}'
    mydict={"q":"country","apikey":get_config("headlines","apikey")}
    if country is not None:
        mydict["country"]=country
    if category is not None:
        mydict["category"]=category
    if records is not None:
        mydict["pageSize"]=records
    #print(url)
    response = requests.get(myurl,params=mydict)
    if response.status_code == 200:
        output = response.json()
        outer_list = []
        for ele in output["articles"]:
            inner_list = (ele["author"], ele["title"])
            outer_list.append(inner_list)
        print(tabulate.tabulate(outer_list,headers=(get_config(section="headlines",option="headers").split(", ")),tablefmt="simple_grid"))
    else:
        print(" Invalid Data")




def main():
    print(" welcome to NEWS API :  ")
    while True:
        print("1.everything api", "2.headlines api", sep='\n')
        choice = input(" Select the required choice :")
        if choice == "1":
            user_choice = input(" Enter the choice  : ")
            print("1.Search in All Fields", "2.Search in Title", "3.search in Description", "4.search in content",
                  sep='\n')
            choice = input(" Enter Search Details :")
            basedon = get_config("search_dict", choice)
            Fromdate, Todate = None, None
            while True:
                Date = input("Do you wish to continue with Date (y/n) : ")
                if Date in ["Y", "y"]:
                    Fromdate = input(" Enter From date (yyyy-mm-dd) :")
                    Todate = input("Enter To date (yyyy-mm-dd)      : ")
                    break
                elif Date in ["N", "n"]:
                    break
                else:
                    print(" Enter either yes or no ")
            Records = None
            while True:
                record = input(" Do you wish to limit the pagecount (y/n) :")
                if record in ["Y", "y"]:
                    Records = input(" enter the page count : ")
                    break
                elif record in ["N", "n"]:
                    break
                else:
                    print(" select either yes or no ")
            everything(user_choice, basedon, Fromdate, Todate, Records)
        elif choice == "2":

            countryDict = {'1': 'ae', "2": "ar", "3": "at", "4": "au", "5": "be", "6": "bg", "7": "br",
                           "8": "ca", "9": "ch", "10": "cn", "11": "co", "12": "cu", "13": "cz", "14": "de",
                           "15": "eg", "16": "fr", '17': "gb", "18": "gr", "19": "hk", "20": "hu",
                           "21": "id", "22": "ie", "23": "il", "24": "in", "25": "it",
                           "26": "jp", "27": "kr", "28": "lt", "29": "lv",
                           "30": "ma", "31": "mx", "32": "my", "33": "ng", "34": "nl", "35": "no",
                           "36": "nz", "37": "ph", "38": "pl", "39": "pt",
                           "40": "ro", "41": "rs", "42": "ru", "43": "sa", "44": "se",
                           "45": "sg", "46": "si", "47": "sk", "48": "th", "49": "tr", "50": "tw",
                           "51": "ua", "52": "us", "53": "ve", "54": "za"}
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
            choice = input(" enter your choice : ")
            country = countryDict[choice]
            categoryDict = {"1": "Business", "2": "Entertainment", "3": "General", "4": "Health", "5": "Science",
                            "6": "Sports", "7": "Technology"}
            print("1.business", "2.entertainment", "3.general", "4.health", "5.science", "6.sports", "7.technology",
                  sep="\n")
            choice1 = input(" enter the choice : ")
            category = categoryDict[choice1]
            Records = None
            while True:
                record = input(" Do you wish to limit the pagecount (y/n) :")
                if record in ["Y", "y"]:
                    record = input(" enter the page count : ")
                    break
                elif record in ["N", "n"]:
                    break
                else:
                    print(" select either yes or no ")

            headlines(country, category, records=None)
        else: print(" Enter Valid Option  ")
        userdecision = input(" Do you wish to continue (y/n) :")
        if userdecision in ["Y", "y"]:
            continue
        else:
            break
main()