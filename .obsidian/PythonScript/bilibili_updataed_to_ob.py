# 需要在Obsidian中安装以下插件
# Shell Commands，用于在Obsidian中实现调用python脚本，以及脚本的自动化运行
# Admonition，美化显示效果
# Obsidian Columns，用于分栏显示结果

# 导入必要的库，也是你需要安装
# 可在cmd中输入pip install xxx(xxx为库名，如requests)
import requests
import re
import json
from pprint import *
import subprocess
import os
import time
from datetime import datetime

# 以下为主体代码，如务必要，请勿自行修改
# 如果有报错，可以在B站给我留言，或者github上提交问题

# 读取cookies
cookie = open("D:/0011 Obsidian存放文件夹/Study/700 Others/cookies.md", 'r', encoding="utf-8").read()
# 设置headers
headers = {
    'referer': 'https://space.bilibili.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
    'cookie': cookie
}

# 获取今天日期
today = str(datetime.now()).split(' ')[0]
# 获取UP信息
def get_up_info(mid):
    url = 'https://api.bilibili.com/x/space/acc/info?mid={}&jsonp=jsonp'.format(mid)
    json_data = json.loads(requests.get(url=url, headers=headers).text)
    name = json_data['data']['name']
    desc = json_data['data']['official']['title']
    sign = json_data['data']['sign']

    url = 'https://api.bilibili.com/x/space/upstat?mid={}&jsonp=jsonp'.format(mid)
    json_data = json.loads(requests.get(url=url, headers=headers).text)
    view = json_data['data']['archive']['view']
    if view > 10000:
        view = '{}w'.format(round(view/10000,2))
    else:
        view = view
    likes = json_data['data']['likes']

    url = 'https://api.bilibili.com/x/relation/stat?vmid={}&jsonp=jsonp'.format(mid)
    json_data = json.loads(requests.get(url=url, headers=headers).text)
    # pprint(json_data)
    follower = json_data['data']['follower']
    if follower > 10000:
        follower = '{}w'.format(round(follower/10000,2))
    else:
        follower = follower
    return [name, view, follower]

# 获取笔记信息
def get_update_info(mid):
    url = 'https://api.bilibili.com/x/space/arc/search?mid={}&pn=1&ps=25&index=1&jsonp=jsonp'.format(mid)
    json_data = json.loads(requests.get(url=url, headers=headers).text)
    if 'data' in json_data:
        vlist = json_data['data']['list']['vlist']
        content = []
        if len(vlist) > 3:
            n = 3
        else:
            n = len(vlist)
        data_list = []
        for i in range(n):
            v = vlist[i]
            created = v['created']
            mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(created)).split(' ')[0]
            title = v['title'][:20]+'……'
            desc = v['description']
            pic = v['pic']
            bvid = v['bvid']
            bilibili_url = 'https://www.bilibili.com/video/{}'.format(bvid)
            vurl = '[{}](https://www.bilibili.com/video/{})'.format(title, bvid)
            author = v['author']
            length = v['length']
            v_content = '![|250]({})\n{}\n🎞时长：{}\n上传时间：{}\n\n'.format(pic,vurl,length,mtime)
            content.append(v_content)
            data_list.append(mtime)
        info = [content,max(data_list)]
    else:
        info = ['这个UP还没有任何更新\n', ' ']

    return info


settings = "D:/0011 Obsidian存放文件夹/Study/700 Others/Python脚本设置.md"
setting = str(open(settings, 'r', encoding="utf-8").read()).replace('\n','').replace(' ','').split('##')
# print(setting)
for i in setting:
    if '关注的UP' in i:
        i = i.split(r'%%')[0]
        mid_list = i.split('-[]')[1:]

with open('关注UP更新.md','w+',encoding='utf-8') as f:
    for i in mid_list:
        # 获取UP信息
        up_info = get_up_info(i)
        name = up_info[0]
        view = up_info[1]
        follower = up_info[2]
        # 视频更新信息
        video_info = get_update_info(i)
        content = video_info[0]
        update_time = video_info[1]    
        f.write('````ad-tip\n')

        # print(update_time)
        if update_time == today:
            f.write('title: **{}**<br>🌹粉丝{}🎞总播放量{}<br>😆UP今天更新了视频\n'.format(name,follower,view))
        elif update_time == ' ':
            f.write('title: **{}**<br>🌹粉丝{}🎞总播放量{}<br>😡{}\n'.format(name,follower,view, content))
        else:
            f.write('title: **{}**<br>🌹粉丝{}🎞总播放量{}<br>😐UP上次更新时间为{}\n'.format(name,follower,view,update_time))
        f.write('```col\n')
        f.write(''.join(content))
        f.write('```\n')
        f.write('````\n')




