import pandas as pd
import json
import numpy as np
import os
import getSteamInfo
from draw import *
from models import *
import collections

#根据最大值把所有数据标准化到0-1之间
def normalize(dictA):
    maxi = np.max(list(dictA.values()))
    dictNew = {}
    for key in dictA.keys():
        dictNew[key]= dictA[key]/maxi
    return dictNew



#从文件夹中读取所有比赛文件（json），这些文件来自http请求 https://pwaweblogin.wmpvp.com/match-api/detail?a=20000&r=177996&s=152064fbe5775f56d8398e555c10777d9bd6d6ac&t=1627114711675的返回json数据
def readMatchesFromFile(path):
    matchInfo = {}
    print("读取比赛文件")
    for root, dirs, files in os.walk(path):
        for file in files:
            print("读取：", os.path.join(root, file))
            with open(os.path.join(root, file), 'r', encoding='utf8') as fp:
                matchJson = json.load(fp)
                matchData = matchJson['data']
                matchId = matchJson['data']['baseInfo']['match']
                if(matchId not in matchInfo.keys()):
                    matchInfo[matchId] = matchData
    return matchInfo

#从文件夹中读取用户文件, 这些文件记录了好友的完美分（score）信息，可用于填充playerInfo
def readPlayerScore(path):
    playerScore={}
    print("读取用户文件")
    for root, dirs, files in os.walk(path):
        for file in files:
            print("读取：", os.path.join(root, file))
            with open(os.path.join(root, file), 'r', encoding='utf8') as fp:
                playerJson = json.load(fp)
                playerUsers = playerJson['data']['users']
                for player in playerUsers:
                    playerId = player['steam_id']
                    score = player['score']
                    if(playerId!=None and playerScore!=None and playerScore!=0):
                        playerScore[playerId]=score
    return playerScore
    

def createPlayerInfo(matchInfo):
    playerInfo = {}
    print("读取比赛信息，录入用户数据")
    for matchId in matchInfo.keys():
        matchData = matchInfo[matchId]
        map = matchData['baseInfo']['map_info']['name_en']
        match_type_id = matchData['baseInfo']['match_type_id']

        for playerTeam in ['Tplayers', 'CTplayers']:
            for playerId in matchData[playerTeam].keys():
                # print(playerId)
                playerMatchData = matchData[playerTeam][playerId]
                if(playerId not in playerInfo.keys()):  # 创建一个新用户
                    playerName = playerMatchData['steam_nick']
                    player = Player(playerId, playerName)
                    playerInfo[playerId] = player
                else:
                    player = playerInfo[playerId]

                if(matchId not in player.matches.keys()):
                    playerInMatch = PlayerInMatch(matchId)
                    playerInMatch.map = map
                    playerInMatch.match_type_id = match_type_id
                    playerInMatch.date = playerMatchData['date']
                    playerInMatch.kill = playerMatchData['kill']
                    playerInMatch.death = playerMatchData['death']
                    playerInMatch.first_kill = playerMatchData['first_kill']
                    playerInMatch.first_death = playerMatchData['first_death']
                    playerInMatch.five_kill = playerMatchData['five_kill']
                    playerInMatch.four_kill = playerMatchData['four_kill']
                    playerInMatch.three_kill = playerMatchData['three_kill']
                    playerInMatch.grenade_tk_num = playerMatchData['grenade_tk_num']
                    playerInMatch.rating = playerMatchData['rating']
                    playerInMatch.rws = playerMatchData['rws']
                    playerInMatch.adpr = playerMatchData['adpr']
                    playerInMatch.score = playerMatchData['score']

                    player.matches[matchId] = playerInMatch



    return playerInfo

#分析用户在十黑中的表现
def player10detail(query_name,playerInfo):
    stats = {}
    for playerId in playerInfo.keys():
        player = playerInfo[playerId]
        if(query_name in player.name):
            #找到用户
            count_ranking = 0
            adpr_ranking = 0

            count_10 = 0
            count_score = 0

            avg_adpr = 0
            avg_score = 0

            for matchId in player.matches.keys():
                match = player.matches[matchId]

                if(match.score!=None):
                    avg_score+=int(match.score)
                    count_score+=1

                if(match.match_type_id=='14'): #十黑
                    avg_adpr+=int(match.adpr)
                    count_10+=1

                if(match.match_type_id=='12'): #天梯
                    adpr_ranking+=int(match.adpr)
                    count_ranking+=1
                
                if(match.match_type_id!='14' and match.match_type_id!='12'):
                    print("match.match_type_id",match.match_type_id)

            
            if(count_10!=0):
                avg_adpr/=count_10
            if(count_score!=0):
                avg_score/=count_score
            if(count_ranking!=0):
                adpr_ranking/=count_ranking

            print("【",player.name,"】\t十黑场数:",count_10,"\t平均十黑ADR:",round(avg_adpr,2),"\t平均天梯分:",round(avg_score),'\t天梯场数:',count_ranking,"\t天梯ADR",adpr_ranking)

            stats['avg_adpr']=avg_adpr
            stats['avg_score']=avg_score

            stats['count_10']=count_10
            stats['count_score']=count_score

            stats['adpr_ranking'] = adpr_ranking
            stats['count_ranking']=count_ranking

            return stats

    print("未找到该用户信息")
    return stats

# 分析十黑内战幻神
# (已弃用)方法是，统计各用户十黑adr，排序，然后获取他们的完美天梯分，排序，两个列表相减后标准化。
# 统计各用户十黑adr和完美天梯分,标准化，相除得到幻神指数
def godIn10(playerInfo,playerScore,forbbidenPlayers=[],method="score"):

    #两个列表，key是用户名,value是对应的十黑adr和天梯分段
    adrDict = {}
    scoreDict = {}
    count_10_Dict = {}
    count_ranking_Dict = {}

    for playerId in playerInfo.keys():
        player = playerInfo[playerId]
        playerStat = player10detail(player.name,playerInfo)

        if(playerStat['count_10']<=2): #10黑场数太少
            continue
            
        if(player.name in forbbidenPlayers): #屏蔽用户名单
            continue
        
        if(method=='ranking'): #使用天梯ADR
            if (playerStat['count_ranking']<=2): #天梯场数太少了
                continue
            else:
                scoreDict[player.name] = playerStat['adpr_ranking']
        else:
            if(playerId in playerScore.keys()): #完美天梯分列表
                scoreDict[player.name] = playerScore[playerId]
            else: 
                if(playerStat['count_score']!=0): #统计天梯排位均分
                    scoreDict[player.name] = playerStat['avg_score']
                else:
                    continue

        adrDict[player.name] = round(playerStat['avg_adpr'],2)
        scoreDict[player.name] = round(scoreDict[player.name],0)
        count_10_Dict[player.name] = playerStat['count_10']
        count_ranking_Dict[player.name] = playerStat['count_ranking']

    # adrDict = collections.OrderedDict(sorted(adrDict,key=lambda s:s[0]))
    # scoreDict = collections.OrderedDict(sorted(scoreDict,key=lambda s:s[0]))


    adrList = sorted(adrDict.items(),key=lambda obj: obj[1])
    scoreList = sorted(scoreDict.items(),key=lambda obj: obj[1])

    print(adrList,scoreList)

    adrStdDict = {}
    scoreStdDict = {}

    godScore =  {}


    # for i in range(0,len(adrDict)):
    #     adrStdDict[adrList[i][0]]=i
    #     scoreStdDict[scoreList[i][0]]=i


        
    if(method=='ranking'):
        adrStdDict = adrDict
        scoreStdDict = scoreDict
    else:
        adrStdDict = normalize(adrDict) 
        scoreStdDict = normalize(scoreDict)


    for playerName in adrStdDict.keys():
        # godScore[playerName] = round(( adrStdDict[playerName]  - scoreStdDict[playerName] + len(adrDict) ) / len(adrDict),2) 
        godScore[playerName] = adrStdDict[playerName]/scoreStdDict[playerName]
        # print("【"+playerName+'】 \t十黑场数: ',count_10_Dict[playerName],'\t平均ADR: ',adrDict[playerName],'\t天梯分: ',scoreDict[playerName],'\t幻神指数: ',godScore[playerName])

    # godScore=normalize(godScore)

    # godList = sorted(godScore.items(),key=lambda obj: obj[1])
    # print(godList)

    # playerNames = ['A','B','C','D','E','F','G']
    # adrs=[1,2,3,4.5,5,6,7.2]
    # godScores = [131, 139, 81, 145, 46, 49, 106]
    # scores = [1107, 1101,1141, 1088, 1046, 1046, 1145]

    playerNames = list(adrStdDict.keys())
    scores = [scoreDict[player] for player in playerNames]
    adrs = [adrDict[player] for player in playerNames]
    godScores = [godScore[player] for player in playerNames]
    count10s = [count_10_Dict[player] for player in playerNames]


    drawGodScoreChart(playerNames,scores,adrs,godScores,count10s,title='SCUTGBT十黑内战幻神',method='ranking')



    

if __name__ == '__main__':
    print(normalize({'a':10,'b':20}))

    matchInfo = {}  # 存储所有比赛信息，实际为json的data字段，内部是嵌套dict
    playerInfo = {}  # 存储每个人的每场比赛的信息，本字典中存储的key为玩家id，values是Player类，Player类中包含一个dict存储PlayerInMatch类

    
    # 存储所有比赛信息
    mathchInfo = readMatchesFromFile('data/matches') 
    # 嵌套字典，存储每个人的每场比赛的信息，本字典中存储的key为玩家id，values是Player类
    playerInfo = createPlayerInfo(mathchInfo)
    # 记录一部分用户的天梯分
    playerScore = readPlayerScore('data/players')

    # player10detail('道与名',playerInfo)
    # player10detail('厕所里蹲',playerInfo)

    #屏蔽列表
    forbbidenPlayers = ['夏工玉']
    godIn10(playerInfo,playerScore,forbbidenPlayers=forbbidenPlayers,method='ranking')


