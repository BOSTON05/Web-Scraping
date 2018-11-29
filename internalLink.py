
from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import urlparse
import re
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pprint

pages = set()
# SSを開く
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'AS-API-032b66c72cc1.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open('AS-data').worksheet('2018')
# キーワードのページ内捜索
# url = int(wks.acell('C3').value)
url = wks.acell('C3').value
# html = urlopen(url)
html = urllib.request.urlopen(url).read().decode('UTF-8')
bs = BeautifulSoup(html, 'html.parser')

# <----------------------------ここまでは多分大丈夫---------------------------------------->

# ページで見つかった全ての内部リンクのリストを取り出す


# includeUrl = urlparse(html).scheme + "://" + urlparse(html).netloc


def getInternalLinks(bs, includeUrl):

    # includeurlをwchemeとnetlocにparseする
    includeUrl = urlparse(includeUrl).scheme + ":/" + \
        urlparse(includeUrl).netloc
    print(urlparse(includeUrl).scheme)
    print(urlparse(includeUrl).netloc)
    internalLinks = []

    # Finds all links that begin with a "/"(内部リンク)
    for link in bs.findAll('a', href=re.compile('^(/|.*'+includeUrl+')')):
        # hrefが存在したら
        if link.attrs['href'] is not None:
            # 新しい内部リンクだったら
            if link.attrs['href'] not in internalLinks:
                # リストに要素を追加
                if(link.attrs['href'].startswith('/')):
                    internalLinks.append(includeUrl+link.attrs['href'])

    return internalLinks

    keyWord = re.findall("募集要項", bs)

    recruitLinks = []

    # if キーワードが存在したら
    if len(keyWord > 0):
        recruitLinks.append(includeUrl+link.attrs['href'])

    return recruitLinks


pprint.pprint(getInternalLinks(bs, html))
# getInternalLinks(bs, html)


#     # urlをssに追記
# wks.update_acell('F3', getInternalLinks)


# print(wks.acell('F3').value)


# # else:
# #     internalLinks.append(link.attrs['href'])
# #     keyWord = re.findall("募集要項", bs)
# #     # if キーワードが存在したら
# #     if len(keyWord > 0):
# #         recruitLinks.append(includeUrl+link.attrs['href'])
# #         # urlをssに追記
# #         wks.update_acell('F3', recruitLinks)
# #         print(wks.acell('F3'))
