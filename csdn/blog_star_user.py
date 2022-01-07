#!/usr/bin/env python
# encoding: utf-8
'''
#-------------------------------------------------------------------
#                   CONFIDENTIAL --- CUSTOM STUDIOS
#-------------------------------------------------------------------
#
#                   @Project Name : 导出2021博客之星给你点赞的用户
#
#                   @File Name    : blog_star_user.py
#
#                   @Programmer   : autofelix
#
#                   @Start Date   : 2022/01/08 14:42
#
#                   @Last Update  : 2022/01/08 14:42
#
#-------------------------------------------------------------------
'''
import os, platform, re, requests
import PySimpleGUI as sg

class csdn:
    def __init__(self):
        pass

def export_score(rid):
    headers = {
        "authority": "mp-action.csdn.net",
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "origin": "https://bbs.csdn.net",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": f"https://bbs.csdn.net/evaluate/{rid}?type=communityCloud&rtype=topic&scoreType=1",
        "accept-language": "zh-CN,zh;q=0.9"
    }
    blog_data = []
    i = 1
    while True:
        params = {
            "page": str(i),
            "size": "20",
            "sortType": "desc",
            "rid": rid,
            "deviceType": "pc",
            "type": "communityCloud",
            "rtype": "topic",
            "scoreType": "1",
            "sortField": "created_At"
        }
        res = requests.get(
            "https://mp-action.csdn.net/interact/wrapper/pc/grade/queryList",
            params=params,
            headers=headers
        )
        data = res.json()['data']
        total = data["total"]
        print(f"{min(i * 20, total)}/{total}", end=",")
        data_list = [(row["nickname"], "https://blog.csdn.net/" + row["username"], str(row["starNum"]))
                     for row in data["list"]]
        blog_data.extend(data_list)
        if i * 20 >= total:
            print()
            print("下载完毕！")
            break
        i += 1
    # df = pd.DataFrame(, columns=["昵称", "csdnid", "评分"])
    return blog_data


sg.change_look_and_feel("Python")
layout = [
    [
        sg.Text("要查询的博客之星topic地址："),
        sg.In(size=(40, 1), key="topic_url", default_text="https://bbs.csdn.net/topics/603955455"),
    ],
    [sg.Button('导出csv文件', enable_events=True, key="export")],
    [sg.Output(size=(65, 9), key="out", text_color="#15d36a")],
    [sg.Text("@小小明：https://bbs.csdn.net/topics/603955455"), ],
]

window_title = '2021博客之星五星评分数据导出'
window = sg.Window(window_title, layout)

while True:
    event, values = window.read()
    if event in (None,):
        break  # 相当于关闭界面
    # print(event, values)
    if event == "export":
        window["out"].update("")
        topic_url = values["topic_url"]
        rids = re.findall("https://bbs.csdn.net/topics/(\d+)", topic_url)
        if not rids:
            sg.popup("提示", "未解析到有效的博客之星投票链接！")
            continue
        filename = sg.popup_get_text("请输入要保存的文件名：", default_text=f"2021博客之星评分_{rids[0]}.csv")
        if not filename:
            continue
        blog_data = export_score(rids[0])
        with open(filename, "w", encoding="gbk") as f:
            f.write("昵称,url,评分\n")
            for a, b, c in blog_data:
                if a.find(",") != -1:
                    a = f'"{a}"'
                f.write(f"{a},{b},{c}".encode("gbk", errors="ignore").decode("gbk"))
                f.write("\n")
        sg.popup("提示", "评分数据导出完毕！")
        print("导出位置：", os.path.abspath(filename))
        platform_system = platform.system()
        if platform_system == "Windows":
            os.system(f"cmd /c start {os.path.abspath(filename)}")
        else:
            os.system(f"open '{os.path.abspath(filename)}'")
