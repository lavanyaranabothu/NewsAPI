import requests
import tabulate
def everything():
    response=requests.get(f'https://newsapi.org/v2/everything?q="Tollywood"&apiKey=4a90cd6aa495440fbaff625f9fe50100&from=2024-01-10&to=2024-01-14&pagesize=50')
    if response.status_code==200:
        output=response.json()
        outer_list=[]
        for ele in output["articles"]:
            inner_list=(ele["source"]["id"],ele["source"]["name"],ele["author"],ele["title"],ele["publishedAt"])
            outer_list.append(inner_list)
            print(tabulate.tabulate(outer_list,headers=("id","name","author","title","publishedAt"),tablefmt="simple_grid"))
    else:
        print(" Invalid Data")

def headlines():
    response=requests.get(f'https://newsapi.org/v2/top-headlines?country=in&apiKey=4a90cd6aa495440fbaff625f9fe50100&pagesize=30&category=entertainment')
    if response.status_code==200:
        output=response.json()
        outer_list=[]
        for ele in output["articles"]:
            inner_list=(ele["source"]["id"],ele["source"]["name"],ele["author"],ele["title"],ele["publishedAt"])
            outer_list.append(inner_list)
            print(tabulate.tabulate(outer_list,headers=("id","name","author","title","publishedAt"),tablefmt="simple_grid"))
    else:
        print(" Invalid Data")

def main():
    print(" WElCOME TO NEWS API ")
    while True:
        print("1.everthing","2.headlines")
        choice=int(input(" Enter the Choice :"))
        if choice==1:
            everything()
        elif choice==2:
            headlines()
        else:
            print('Invalid Selection, please select right option')
        userdecision=input(" Enter the USer Decision (y/n) : ")
        if userdecision in ['y' or 'Y']:
            continue
        else: break
main()



