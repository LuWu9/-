import urllib.request
import os
import re
import tkinter as tk

root = Tk()


root_url = "http://www.biquge.com"

def open_url(url): # 用于打开小说目录网址(传入主网址)
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0')
    # print(url)
    response = urllib.request.urlopen(req)
    html = response.read()

    return html

def get_eachu(url): # 获取小说每章的网址和标题(传入主网址)
    html = open_url(url).decode('utf-8')

    title_side = re.search(r"<dt>(.+)</dt>",html).span()
    html = html[title_side[0]+225:]
    title_side = re.search(r"<dt>(.+)</dt>",html).span()
    html = html[title_side[0]:]
    
    each_url = re.findall(r"<a href=\"(.+?)\"",html)
    return each_url

def get_eacht(url): # 获取小说每章的网址和标题(传入主网址)
    html = open_url(url).decode('utf-8')

    title_side = re.search(r"<dt>(.+)</dt>",html).span()
    html = html[title_side[0]+225:]
    title_side = re.search(r"<dt>(.+)</dt>",html).span()
    html = html[title_side[0]:]
    
    each_title = re.findall(r"\">(.+?)</a>",html)
    return each_title

def get_title(url): # 获取小说标题(传入主网址)
    html = open_url(url).decode('utf-8')
    title_side = re.search(r"<h1>(.+)</h1>",html).span()
    title = html[title_side[0]+4:title_side[1]-5]
    return title
    
def get_sub(url): # 获取小说内容(传入分网址)
    html = open_url(url).decode('utf-8')
    readx_side = re.search(r"readx",html).span()
    chap_side = re.search(r"chaptererror",html).span()
    a = readx_side[1] + 18
    b = chap_side[0] - 8
    each_sub = html[a:b]
    each_sub = re.sub(r"\"","",each_sub)
    each_sub = re.sub(r"<br/>","\n",each_sub)
    return each_sub

def whole_chapter(url): # 当用户选择全部下载时(传入主网址)
    filename = get_title(url)
    with open(filename+".txt",'wb') as f:
        for i in range(len(each_url)):
            print(each_title[i]+"   正在下载")
            each_sub = ("\n"+each_title[i]+"\n"+"\n"+get_sub(root_url+each_url[i])).encode()
            f.write(each_sub)

def each_chapter(url): # 分节下载(传入主网址)
    second_folder = get_title(url)
    try:
        os.mkdir(second_folder) # 创建笔趣阁下载主文件夹
    except FileExistsError:
        os.chdir(second_folder) # 切换到工作目录下
    else:
        os.chdir(second_folder)
        
    for i in range(len(each_url)):
        filename = each_title[i]
        with open(filename+".txt",'wb') as f:
            print(each_title[i]+"   正在下载")
            each_sub = get_sub(root_url+each_url[i]).encode()
            f.write(each_sub)

# def download_novels(folder='bqg_dl'): # (传入主网址)
    """创建主要的工作目录"""
folder='bqg_dl'
try:
    os.mkdir(folder) # 创建笔趣阁下载主文件夹
except FileExistsError:
    os.chdir(folder) # 切换到工作目录下
else:
    os.chdir(folder)

get_url = input() # 获取用户输入的网址(窗口)
each_url = get_eachu(get_url) # 每章的网址
each_title = get_eacht(get_url) # 每章的标题
#print(each_url)
each_chapter(get_url)

#if __name__ == '__main__':
    #download_novels()
