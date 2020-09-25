# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 16:05:54 2018

@author: 井鱼
"""

import requests
import re
import json
from requests.exceptions import RequestException
import numpy as np
import pandas as pd

def get_one_page(url,header):
    try:
        response = requests.get(url,headers = header)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None
    
# 解析网页（正则表达式）
def parse_one_page1(html):
    each_list = []
    
    pattern1 = re.compile('_list"><ahref=".(.*?)"class="list-group-item"title=', re.S)
    items1 = re.findall(pattern1,html.replace('\n', '').replace('\t', '').replace(' ', ''))
    each_list.append(items1[0])
    
    pattern2 = re.compile('<a href=".(.*?)".*?class="list-group-item"', re.S)
    items2 = re.findall(pattern2, html)
    for i in range(1, len(items2)):
        each_list.append(items2[i])
    return each_list
                    
def write_to_file(content):
    pass

def main(index):
    if (index == 0):
        main_url = "http://www.mot.gov.cn/shuiluchuxing/zhujiangshuiqingxinxi/index.html"
    else:
        main_url = "http://www.mot.gov.cn/shuiluchuxing/zhujiangshuiqingxinxi/index_" + str(index) + ".html"
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; \x64) AppleWebKit/537.36\
              (KHTML, like Gecko)\
              Chrome/71.0.3578.98 Safari/537.36'}
    html = get_one_page(main_url,header)
    each_list = parse_one_page1(html)
    return each_list
    
def get_data(url, i):
    sub_url = "http://www.mot.gov.cn/shuiluchuxing/zhujiangshuiqingxinxi" + url
    
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; \x64) AppleWebKit/537.36\
              (KHTML, like Gecko)\
              Chrome/71.0.3578.98 Safari/537.36'}
    html = get_one_page(sub_url,header)
    
    return parse_one_page2(html, i)

def parse_one_page2(html, i):
    
    if (i < 44):
        pattern1 = re.compile('<tr style="height:.*?><td.*?px;">(.*?)</span></p></td><td.*?px;">(.*?)</span></p></td><td.*?px;">(.*?)</span><span.*?px;">(.*?)</span></p></td><td.*?px;">(.*?)</span></p></td><td.*?px;">(.*?)</span></p></td><td.*?px;">(.*?)</span></p></td></tr>', re.S)
        items = re.findall(pattern1,html)
    else:
        #44开始，格式变了
        pattern2 = re.compile('<tr style="height: 18.75pt">.*?color: black">(.*?)</span></p>.*?<td.*?color: black">(.*?)</span></p>.*?<td .*?color: black">(.*?)</span><span .*?lang="EN-US">(.*?)</span>.*?lang="EN-US">(.*?)</span>.*?lang="EN-US">(.*?)</span></span></p>.*?<td.*?color: black">(.*?)</span></p>.*?<td.*?color: black">(.*?)</span></p>.*?<td.*?color.*?">(.*?)</span></p>.*?</tr>', re.S)
    
        #pattern3 = re.compile('<tr style="height: 18.75pt">(.*?)</tr>', re.S)
        print(html)
        items = re.findall(pattern2,html)
        print(items)
        items = transfer(items)
        print(items)
    return items
    

def transfer(items):
    new_items = []
    for item in items:
        item = list(item)
        new_item = []
        str1 = str(item[2]) + "年" + str(item[3]) + "月" + str(item[4]) + "日" + item[5]
        item0 = ''.join(re.findall('[\u4e00-\u9fa5]',item[0]))
        new_item.append(item0)
        new_item.append(item[1])
        new_item.append(str1)
        new_item.append(item[6])
        new_item.append(item[7])
        new_item.append(item[8])
        new_items.append(tuple(new_item))
    return new_items


if __name__ == "__main__":
    '''url_list = []
    for i in range(0, 17):
        each_list = main(i)
        for each in each_list:
            url_list.append(each)
            
    print(url_list)
    url=np.array(url_list)
    np.save('url.npy', url)'''
    
    url = np.load("url.npy")
    url_list = url.tolist()
 
    # 开始爬取哈
    #print(url_list[145])
    print(get_data(url_list[136], 1000))
    '''
    all_list = []
    
    i = 0
    for url in url_list:
        print(i)
        items = get_data(url, i)
        print(items)
        for item in items:
            all_list.append(item)
        i = i + 1
        
    np.save("data.npy", np.array(all_list))'''
    
    data = np.load("data.npy")
    print(len(data.tolist()))
    #44 空
    
    result = []
    for one in data:
        result.append(list(one))
    print(result)
    #name=['站名','河名','时间','水位（m）','流量（m3/s）','水势']
    #test=pd.DataFrame(data=result)#数据有三列，列名分别为one,two,three
    #print(test)
    #test.to_csv('data.csv',encoding='gbk')
    



























































    