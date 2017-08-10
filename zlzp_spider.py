#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib.parse import quote
from bs4 import BeautifulSoup
from zlzp_city import citys
import requests
import time
import csv
import re


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 '
}
types = ['160000', '160300', '160400', '200500', '200300', '5001000']


def add_job(url):
    urls_list = [url.format(quote(pn)+'&jl={}') for pn in types]
    add_city(urls_list)


def add_city(urls_list):
    for i in urls_list:
        urls_list = [i.format(quote(pn)+'&p=') for pn in citys]
    get_page(urls_list)


def get_page(urls_list):
    suc = 0
    error = 0
    for url in urls_list:
        i = url
        time.sleep(2)
        try:
            f = open('qg_all_url.csv', 'a', newline='')
            writer = csv.writer(f)
            html = requests.get(url, headers=headers).text
            soup = BeautifulSoup(html, 'lxml')
            page = soup.find(class_='search_yx_tj')
            page = str(page.em)
            page = re.sub('<.*?>', '', page)
            page = int(page)/60
            page = int(page)
            if page > 90:
                page = 91
            elif page <= 1:
                page = 2
            else:
                page = page+1
            for j in range(1, page):
                page_list = []
                k = i + str(j)
                page_list.append(k)
                print(page_list)
                writer.writerow(page_list)
                suc += 1
                print(f"成功写入第{suc:d}条数据")
            f.close()
        except Exception as e:
            error += 1
            print(e)
    print(f"成功{suc:d}")
    print(f"失败{error:d}")


def zw_url():
    all_urls = []
    f = open('qg_all_url.csv', 'r')
    reader = csv.reader(f)
    for i in reader:
        all_urls.append(i)
    f.close()
    suc = 0
    error = 0
    for url in all_urls:
        time.sleep(2)
        try:
            f = open('zw_all_url.csv', 'a', newline='')
            writer = csv.writer(f)
            url = url[0]
            html = requests.get(url, headers=headers).text
            soup = BeautifulSoup(html, 'lxml')
            for items in soup.find_all(class_='zwmc'):
                pat = str(items.a)
                pat1 ='<a href="(.*?)" par='
                listq = re.findall(pat1, pat)
                writer.writerow(listq)
                suc += 1
                print(f"成功写入第{suc:d}条数据")
            f.close()
        except Exception as e:
            error += 1
            print(e)
            pass
    print(f"成功{suc:d}")
    print(f"失败{error:d}")


def get_zwxx():
    all_urls = []
    f = open('zw_all_url.csv', 'r')
    reader = csv.reader(f)
    for i in reader:
        all_urls.append(i)
    f.close()

    f = open('zwxx.csv', 'a', newline='')
    writer = csv.writer(f)
    writer.writerow(['职位', '公司', '工资', '工作地点', '发布时间', '职位性质', '工作经验', '学历', '招聘人数', '职位类别'])
    f.close()

    suc = 0
    error = 0
    for url in all_urls:
        try:
            time.sleep(2)
            f = open('zwxx.csv', 'a', newline='')
            writer = csv.writer(f)
            if url == '':
                continue
            else:
                url = url[0]
            html = requests.get(url, headers=headers).text
            soup = BeautifulSoup(html, 'lxml')
            zwlist = []
            try:
                for mc in soup.find_all(class_='inner-left fl'):
                    zw = str(mc.h1)
                    zw = re.sub('<.*?>', '', zw)
                    zw = re.sub('『.*?』', '', zw)
                    zw = re.sub('【.*?】', '', zw)
                    zw = re.sub('（.*?\)', '', zw)
                    zw = re.sub('\(.*?\)', '', zw)
                    zw = re.sub('\(.*?）', '', zw)
                    zw = re.sub('（.*?）', '', zw)
                    zwlist.append(zw)
                    gs = str(mc.a)
                    gs = re.sub('<.*?>', '', gs)
                    gs = re.sub('『.*?』', '', gs)
                    gs = re.sub('【.*?】', '', gs)
                    zwlist.append(gs)
                for xx in soup.find_all(class_='terminal-ul clearfix'):
                    yx = str(xx)
                    pat1 ='<li><span>(.*?)</span><strong>(.*?)</strong></li>'
                    listq = re.findall(pat1,yx)
                    for i in listq:
                        n = list(i)
                        i = re.sub(' ', '', n[1])
                        i = re.sub('<.*?>', '', i)
                        i = re.sub('『.*?』', '', i)
                        i = re.sub('【.*?】', '', i)
                        zwlist.append(i)
                    print(zwlist)
                    writer.writerow(zwlist)
                    suc += 1
                    print(f"成功写入第{suc:d}条数据")
            except Exception as e:
                error += 1
                print(e)
                pass
            f.close()
        except Exception as e:
            error += 1
            print(e)
            print('数据连接出现问题休息十分钟')
            time.sleep(600)
            pass
    print(f"成功输入{suc:d}")
    print(f"失败输入{error:d}")


if __name__ == '__main__':
    start_url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?bj={}'
    add_job(start_url)
    zw_url()
    get_zwxx()
