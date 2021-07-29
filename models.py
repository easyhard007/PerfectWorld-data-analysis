#类

class Player:
    id = -1
    name = ''
    
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.matches = {} #字典，key为比赛id，value为玩家比赛类



#玩家比赛类，只记录一个玩家在一场比赛中的数据
class PlayerInMatch:
    id = -1
    map = ''
    date = '0'
    match_type_id = -1 #14：自定义比赛  12：天梯
    kill=0
    death = 0
    first_kill = 0
    first_death=0
    five_kill = 0
    four_kill = 0
    three_kill = 0
    grenade_tk_num=0
    rating=0
    rws=0
    adpr=0
    score=-1 #打这场比赛时的段位分


    def __init__(self, id):
        self.id = id

class Test():
    a = 0
    def __init__(self):
        self.d = {}


