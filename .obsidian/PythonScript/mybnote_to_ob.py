# 需要在Obsidian中安装以下插件
## Shell Commands，用于在Obsidian中实现调用python脚本，以及脚本的自动化运行

# 导入必要的库，也是你需要安装
# 可在cmd中输入pip install xxx(xxx为库名，如requests)
import requests
import re
import json
from pprint import *
import subprocess
import os

# 以下为主体代码，如务必要，请勿自行修改
# 如果有报错，可以在B站给我留言，或者github上提交问题

# 读取cookies
cookie = open("700 功能性文件/cookies.md", 'r', encoding="utf-8").read()

headers = {
    'referer': 'https://space.bilibili.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
    'cookie': cookie
}

def mkdir(path):
    #判断目录是否存在
    #存在：True
    #不存在：False
    folder = os.path.exists(path)

    #判断结果
    if not folder:
        os.makedirs(path)

    else:
        pass
# 创建文件夹
mkdir('800 附件')
path_one = '400 B站视频笔记'
mkdir(path_one)

# 获取笔记信息
def get_note_content(bvid, note_id):
    url = 'https://api.bilibili.com/x/note/info?oid=383651210&oid_type=0&note_id={}&csrf=05c5773ff1021244939b9fbfa0a8e086'.format(note_id)
    json_data = json.loads(requests.get(url=url, headers=headers).text)
    content = json.loads(json_data['data']['content'])
    # pprint(json_data)
    note_content = []
    for i in content:
        line_content = i["insert"]
        # pprint(line_content)
        if type(line_content) == str:
            note_content.append(line_content)
        elif type(line_content) == dict:
            if 'tag' in line_content:
                desc = line_content['tag']['desc']
                seconds = line_content['tag']['seconds']
                m,s = divmod(seconds,60)
                h,m = divmod(m,60)
                time = '{}:{}:{}'.format(h,m,s)
                timestemp = '[{} {}](https://www.bilibili.com/video/{}#t={})'.format(time,desc,bvid,seconds)
                note_content.append(timestemp)
            if 'imageUpload' in line_content:
                img_id = line_content['imageUpload']['id']
                img_url = 'http:'+line_content['imageUpload']['url']
                img = requests.get(url=img_url, headers=headers)
                with open('800 附件/{}.png'.format(img_id),'wb') as f:
                    f.write(img.content)
                image = '![](800%20附件/{}.png)'.format(img_id)
                note_content.append(image)
    return note_content

# 获取笔记ID
url = 'https://api.bilibili.com/x/note/list?pn=1&ps=10&csrf=05c5773ff1021244939b9fbfa0a8e086'
json_data = json.loads(requests.get(url=url, headers=headers).text)
pprint(json_data)
for i in json_data['data']['list']:
    video_info = i['arc']
    bvid = i['arc']['bvid']
    update_time = i['mtime']
    note_id = i['note_id']
    video_url = 'https://www.bilibili.com/video/{}'.format(bvid)
    title = i['title'].replace('：','-').replace('|','-').replace('【','(').replace('】',')').replace('！','').replace(' ','')
    note_content = get_note_content(bvid,note_id)
    # 判断笔记是否已经存在
    md = os.path.exists('{}.md'.format(title))
    if not md:
        with open('{}/{}.md'.format(path_one,title), 'w', encoding="utf-8") as f:
            f.write('---\ntitle: {}\ncreate at: {}\nvideo url: {}\n---\n'.format(title,update_time,video_url))
            f.write('# {}\n'.format(title))
            f.write('## 原视频\n[{}]({})\n'.format(title, video_url))
            f.write('## 笔记内容\n')
            for i in note_content:
                f.write(i)
    else:
        pass



