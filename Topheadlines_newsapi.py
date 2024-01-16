import tabulate
import requests

def headlines():
    response = requests.get(f'https://newsapi.org/v2/top-headlines?country=us&apiKey=d66a2c5691fe4db1826283f00030b28e')
    if response.status_code == 200:
        output = response.json()
        outer_list = []
        for ele in output['articles']:
            inner_list = (ele['source']['id'],ele['source']['name'], ele['author'],ele['title'],ele['description'],ele['url'],ele['urlToImage'],ele['publishedAt'],ele['content'])
            outer_list.append(inner_list)
            print(tabulate.tabulate(outer_list, headers=('id','name','author','title','description','url','urlToImage','publishedAt','content'),tablefmt= 'simple_grid'))
    else:
        print('invalid data')

headlines()