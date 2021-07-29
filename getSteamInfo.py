# -----------通过team id获取steam昵称-----------方法是抓取个人资料页面: https://steamcommunity.com/profiles/7656XXXXXXXXXXXXX
# 注意steam个人资料页面国内不一定打得开，最好挂vpn，否则可能连接失败


import requests        #导入requests包
from bs4 import BeautifulSoup
from multiprocessing import Pool

def getSteamNameById(id):
    url_pref='https://steamcommunity.com/profiles/'
    url = url_pref+id
    try:
        strhtml=requests.get(url)
    except:
        print('Cannot connect to:',url)
        return ''
    soup=BeautifulSoup(strhtml.text)
    try:
        data = soup.select('body > div.responsive_page_frame.with_header > div.responsive_page_content > div.responsive_page_template_content > div > div.profile_header_bg > div > div > div > div.profile_header_centered_persona > div.persona_name > span.actual_persona_name')[0].text
        return data
    except IndexError:
        print("Cannot find user by this id")
        return ''

def getSteamProfilePage(url):
    try:
        strhtml=requests.get(url)
        return strhtml
    except:
        print('Cannot connect to:',url)
        return ''

#多线程爬取，返回一个字典{steam_id:steam昵称}
def getMultiSteamNameByIdList(idList):
    url_pref='https://steamcommunity.com/profiles/'
    urlList = []
    for id in idList:
        urlList.append(url_pref+str(id))
    print(urlList)
    pool = Pool(processes=8)
    pageHtmlList = pool.map(getSteamProfilePage,urlList)
    pool.close()
    pool.join()
    print(pageHtmlList)
    names = []
    for pageIndex in range(0,len(pageHtmlList)):
        pageHtml = pageHtmlList[pageIndex]
        try:
            soup=BeautifulSoup(pageHtml.text)
        except:
            print("Webpage parse error")
            names.append('')
            continue

        try:
            data = soup.select('body > div.responsive_page_frame.with_header > div.responsive_page_content > div.responsive_page_template_content > div > div.profile_header_bg > div > div > div > div.profile_header_centered_persona > div.persona_name > span.actual_persona_name')[0].text
            names.append(data)
        except IndexError:
            print("Cannot find user by this id")
            names.append('')
            continue
    
    if(len(names)!=len(idList)):
        print("返回结果数量有误")
        return {}
    nameDict = {}
    for i in range(0,len(idList)):
        id = idList[i]
        name = names[i]
        nameDict[id] = name
    print(nameDict)
    return nameDict



if __name__ == '__main__':
    print(getSteamNameById('76561198018254473'))
#     idList = []
#     for i in range(73,99):
#         idList.append('765611980182544'+str(i)) 
#     idList.append('765611980182544')
#     getMultiSteamNameByIdList(idList)