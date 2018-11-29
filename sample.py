# # ! python3
# # luckey.py

import requests
import sys
import webbrowser
import bs4

print('Googlling...')

# sys.argvファイル名とコマンドライン引用のリストが格納
res = requests.get('http://google.com/search?q=' + 'python'.join(sys.argv[1:]))
res.raise_for_status()

# 上位の検索結果のリンクを取得する
soup = bs4.BeautifulSoup(res.text, 'html5lib')
link_elems = soup.select('.r a')

# 各結果をブラウザのタブで開く
num_open = min(5, len(link_elems))
for i in range(num_open):
    webbrowser.open('http://google.com' + link_elems[i].get('href'))


# import requests
# import bs4

# res = requests.get('http://nostarch.com')
# res.raise_for_status()
# no_starch_soup = bs4.BeautifulSoup(res.text)
# type(no_starch_soup)


# import bs4
# example_file = open('sample.html')
# ezample_soup = bs4.BeautifulSoup(example_file)
# elems = sample_soup.select('#author')
# print(elems)
