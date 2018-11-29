from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import urlparse
import re
import datetime
import random

# try:
#     html = urlopen('http://www.pythonscraping.com/pages/page1.html')
# except HTTPError as e:
#     print(e)
# except URLError as e:
#     print('The server could not be found!')
# else:
#     print('It worked!')


# def getlinks(pageUrl):
#     global pages

#     html = urlopen('http://en.wikipedia.org' + pageUrl)
#     bsObj = BeautifulSoup(html, 'html5lib')

#     try:
#         print(bsObj.h1.get_text())
#         print(bsObj.find(id="mw-content-text").findAll("p")[0])
#         print(bsObj.find(id="ca-edit").find("span").find("a").attrs['href'])
#     except AttributeError:
#         print("this page is missing something! No worries though!")

#     for link in bsObj.findAll("a", href=re.compile("^(/wiki/)")):
#         if 'href' in link.attrs:
#             if link.attrs['href'] not in pages:
#                 # 新しいページにあった
#                 newPage = link.attrs['href']
#                 print("-----------\n"+newPage)
#                 pages.add(newPage)
#                 getlinks(newPage)


# getlinks("")


pages = set()
random.seed(datetime.datetime.now())

# ページで見つかった全ての内部リンクのリストを取り出す


def getInternalLinks(bs, includeUrl):
    # includeurlをwchemeとnetlocにparseする
    includeUrl = urlparse(includeUrl).scheme+"://"+urlparse(includeUrl).netloc
    internalLinks = []
    # Finds all links that begin with a "/"(内部リンク)
    for link in bs.find_all('a', href=re.compile('^(/|.*'+includeUrl+')')):
        # hrefが存在したら
        if link.attrs['href'] is not None:
            # 新しい内部リンクだったら
            if link.attrs['href'] not in internalLinks:
                # リストに要素を追加
                if(link.attrs['href'].startswith('/')):
                    internalLinks.append(includeUrl+link.attrs['href'])
                else:
                    internalLinks.append(link.attrs['href'])
    return internalLinks

# ページで見つかった全ての外部リンクのリストを取り出す


def getExternalLinks(bs, excludeUrl):
    externalLinks = []
    # Finds all links that start with "http" that do not contain the current URL
    for link in bs.find_all('a', href=re.compile('^(http|www)((?!'+excludeUrl+').)*$')):
        # 外部リンクがあったら
        if link.attrs['href'] is not None:
            # 外部リンクがあったら
            if link.attrs['href'] not in externalLinks:
                # 外部リンク取得
                externalLinks.append(link.attrs['href'])
    return externalLinks

# ランダムな外部リンク


def getRandomExternalLink(startingPage):
    html = urlopen(startingPage)
    bs = BeautifulSoup(html, 'html.parser')
    externalLinks = getExternalLinks(bs, urlparse(startingPage).netloc)
    # externalLinksがなかったら
    if len(externalLinks) == 0:
        print('No external links, looking around the site for one')
        # 内部リンクを取得
        domain = (urlparse(startingPage).scheme +
                  "://" + urlparse(startingPage).netloc)
        internalLinks = getInternalLinks(bs, domain)
        return getRandomExternalLink(internalLinks[random.randint(0, len(internalLinks)-1)])
    #  externalLinksがあったら
    else:
        return externalLinks[random.randint(0, len(externalLinks)-1)]

# ランダムな外部リンクを返す


def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite)
    print("Random external link is: " + externalLink)
    followExternalOnly(externalLink)


followExternalOnly('http://oreilly.com')
