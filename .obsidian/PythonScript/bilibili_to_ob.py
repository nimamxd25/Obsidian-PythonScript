import requests
import json
import os

headers = {
    'referer': 'https://space.bilibili.com/18225929/favlist?fid=articles',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50',
    'cookie':  ## 自行添加
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

def write_note(bvid,folder_path,path_two,path_three):
    s = requests.session()
    vid = json.loads(s.get('https://api.bilibili.com/x/web-interface/view?bvid='+bvid,headers=header).text)
    if 'BV' not in url:
        with open('error.md', 'w', encoding="utf-8") as f:
            f.write('暂时不支持此类型连接，请不要用此脚本爬取B站番剧和电影等，或者用于其他网站')
    elif 'ugc_season' not in vid['data']:
        bvid = vid['data']['bvid']
        title = vid['data']['title']
        video_url = 'https://www.bilibili.com/video/{}'.format(bvid)
        line = '- [ ] [{}]({})\n'.format(title, video_url)
        print(line)
        with open('{}/{}.md'.format(path_one, title), 'w', encoding="utf-8") as f:
            f.write('---\ntarget: tasks\nstatus: in progress\ntags: bilibili\n---\n')
            f.write('# 学习视频\n')
            f.write(line)
            f.write('# 笔记\n')
    else:
        ep = vid['data']['ugc_season']['sections'][0]['episodes']
        epname = vid['data']['ugc_season']['title']
        cover = vid['data']['ugc_season']['cover']
        path_two = '{}/{}'.format(path_one,epname)
        path_three = '{}/{}'.format(path_two,'笔记')
        mkdir(path_two) 
        mkdir(path_three)
        for i in ep:
            title = i['title']
            bvid = i['bvid']
            video_url = 'https://www.bilibili.com/video/{}'.format(bvid)
            with open('{}/{}.md'.format(path_three, title), 'w', encoding="utf-8") as f:
                f.write('# 学习视频\n')
                line = '[{}]({})\n'.format(title, video_url)
                f.write(line)
                f.write('# 笔记\n')       

        with open('{}/{}.md'.format(path_two,epname), 'a', encoding="utf-8") as f:
            # f.write('---\n')
            # f.write('banner: {}\n'.format(cover))
            f.write('---\ntarget: tasks\nstatus: in progress\ntags: bilibili\n---\n')
            f.write('# 学习清单\n')
            for i in ep:
                f.write('- [ ] [[{}]]\n'.format(i['title']))

def bilibili_to_ob(path_one,url):
    # 创建笔记文件夹
    # path_one = '100 B站视频'
    mkdir(path_one)
    # 爬取同步收藏夹内容
    response = requests.get(url=url, headers=headers)
    json_data = json.loads(response.text)
    medias = json_data['data']['medias']
    for i in medias:
        # 获取新的爬取链接
        bvid = i['bvid']
        new_url = 'https://api.bilibili.com/x/web-interface/view?bvid={}'.format(bvid)
        vid = json.loads(requests.get(url=new_url, headers=headers).text)
        print(vid)
        if 'ugc_season' not in vid['data']:
            bvid = vid['data']['bvid']
            title = vid['data']['title']
            video_url = 'https://www.bilibili.com/video/{}'.format(bvid)
            line = '- [ ] [{}]({})\n'.format(title, video_url)
            # 判断笔记是否已经存在
            note = os.path.exists('{}/{}.md'.format(path_one, title))
            if not note:
                with open('{}/{}.md'.format(path_one, title), 'w', encoding="utf-8") as f:
                    f.write('---\ntarget: tasks\nstatus: in progress\ntags: bilibili\n---\n')
                    f.write('# 学习视频\n')
                    f.write(line)
                    f.write('# 笔记\n')
                    print('{} 视频已同步！'.format(title))
        else:
            ep = vid['data']['ugc_season']['sections'][0]['episodes']
            epname = vid['data']['ugc_season']['title']
            cover = vid['data']['ugc_season']['cover']
            # 创建对应文件夹
            path_two = '{}/{}'.format(path_one,epname)
            path_three = '{}/{}'.format(path_two,'笔记')
            # 判断文件夹是否已经存在
            folder = os.path.exists(path_two)
            if not folder:
                # 如果不存在，则创建新目录
                os.makedirs(path_three)
                for i in ep:
                    title = i['title']
                    bvid = i['bvid']
                    video_url = 'https://www.bilibili.com/video/{}'.format(bvid)
                    with open('{}/{}.md'.format(path_three, title), 'w', encoding="utf-8") as f:
                        f.write('# 学习视频\n')
                        line = '[{}]({})\n'.format(title, video_url)
                        f.write(line)
                        f.write('# 笔记\n') 
                print('{} 视频已同步！'.format(epname))

                with open('{}/{}.md'.format(path_two,epname), 'a', encoding="utf-8") as f:
                    # f.write('---\n')
                    # f.write('banner: {}\n'.format(cover))
                    f.write('---\ntarget: tasks\nstatus: in progress\ntags: bilibili\n---\n')
                    f.write('# 学习清单\n')
                    for i in ep:
                        f.write('- [ ] [[{}]]\n'.format(i['title']))

def get_id(name):
    # 获取mid
    url = 'https://api.bilibili.com/x/web-interface/nav'
    json_data = json.loads(requests.get(url=url, headers=headers).text)
    mid = json_data['data']['mid']
    # 获取
    url = 'https://api.bilibili.com/x/v3/fav/folder/created/list-all?up_mid={}&jsonp=jsonp'.format(mid)
    json_data = json.loads(requests.get(url=url, headers=headers).text)
    id_list = []
    title_list = []
    for i in json_data['data']['list']:
        id_ = i['id']
        title = i['title']
        id_list.append(id_)
        title_list.append(title)
    dic = dict(zip(title_list, id_list))
    print(dic)
    return dic[name]


# 收藏夹名字
settings = "D:/0011 Obsidian存放文件夹/Study/700 功能性文件/Python脚本设置.md"
setting = str(open(settings, 'r', encoding="utf-8").read()).replace('\n','').replace(' ','')
      
names = re.findall('##B站同步文件夹(.*?)##', setting)[0].split('-[]')
names = [i for i in names if i != '']
for name in names:
    # name = 'Obsidian同步收藏夹'
    id_ = get_id(name)
    url = 'https://api.bilibili.com/x/v3/fav/resource/list?media_id={}&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp'.format(id_)
    path_one = '100 B站视频/{}'.format(name)
    ok = bilibili_to_ob(path_one,url)
