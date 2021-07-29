# 本项目遵循GNU开源协议


【SCUTGBT】本项目主要用于分析参与完美对战平台十黑的玩家的幻神水平和演员水平
作者：陈奕男 华南理工大学GBT电竞社

目的：有些人在天梯很强，打十黑的时候却是演员；有些人天梯的时候很拉胯，十黑的时候却疯狂虐杀，人称内战幻神。通过抓取完美对战平台的数据，分析哪些是内战幻神，哪些是内战演员
算法主要思想：获取每个玩家在天梯（match_type_id='12'）和十黑(match_type_id='14')的场均ADR并相除



需要使用fiddler抓取完美对战平台的比赛数据，抓取内容包括：
1. 用户好友列表
http请求为https://pwaweblogin.wmpvp.com/api-user/get-by-steam-ids?a=20000&r=415406&s=e34ea18944ef62e85ddc0f361bba08dda445a869&t=1627533260245 
返回json数据，将被存储到data\players文件夹

2. 比赛详细信息（需要在数据-比赛记录中，点开具体的比赛）
http请求为https://pwaweblogin.wmpvp.com/match-api/detail?a=20000&r=851266&s=fcaac451417c6d2c6df4bcdad37345ce871b11c8&t=1627533349096
返回json数据，将被存储到data\matches文件夹

需要定制更多需求的可以联系我的qq：452124856

