#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import time
import csv
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 '
}


def get_work_url():
    f = open('zw_all_url.csv', 'a', newline='')
    writer = csv.writer(f)
    x = 0
    url = 'https://www.lagou.com/'
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    zw_urls = soup.find(class_='menu_sub dn')
    zw_urls = str(zw_urls)
    pat = '<a class=.*? data-lg-tj-id=.*? data-lg-tj-no=.*? href="(.*?)">.*?</a>'
    zw_urls = re.findall(pat, zw_urls)

    for zw in zw_urls:
        zw_list = [zw]
        writer.writerow(zw_list)
        x = x + 1
        print(f"成功输入第{x:d}条")

    f.close()


def get_page_url():
    all_urls = []
    f = open('zw_all_url.csv', 'r')
    reader = csv.reader(f)
    for i in reader:
        all_urls.append(i)
    f.close()

    suc = 0
    error = 0
    for url in all_urls:
        try:
            f = open('zwpage_all_url.csv', 'a', newline='')
            writer = csv.writer(f)
            time.sleep(5)
            html = requests.get(url[0], headers=headers).text
            soup = BeautifulSoup(html, 'lxml')
            page = soup.find(class_='span totalNum')
            page = str(page)
            pat = '<span class="span totalNum">(.*?)</span>'
            page = re.findall(pat, page)
            try:
                for page in page:
                    page = int(page) + 1
                    urls = [url[0] + str(pn) for pn in range(1, page)]
                    for page_url in urls:
                        page_list = [page_url]
                        writer.writerow(page_list)
                        suc += 1
                        print(page_url)
                        print(f"成功写入第{suc:d}条数据")
            except:
                error += 1
                pass
            f.close()
        except:
            error += 1
            time.sleep(600)
            print("数据连接出现问题休息十分钟")
            pass
    print(f"成功输入{suc:d}")
    print(f"失败输入{error:d}")


def get_zw_url():
    all_urls = []
    f = open('zwpage_all_url.csv', 'r')
    reader = csv.reader(f)
    for i in reader:
        all_urls.append(i)
    f.close()

    suc = 0
    error = 0
    for url in all_urls:
        try:
            f = open('zwxx_all_url.csv', 'a', newline='')
            writer = csv.writer(f)
            time.sleep(20)
            print(url[0])
            html = requests.get(url[0], headers=headers).text
            soup = BeautifulSoup(html, 'lxml')
            zwxx_url = soup.find_all(class_='position_link')
            zwxx_url = str(zwxx_url)
            pat = 'href="(.*?)"'
            zwxx_urls = re.findall(pat, zwxx_url)
            try:
                for i in zwxx_urls:
                    konglist = [i]
                    writer.writerow(konglist)
                    suc += 1
                    print('成功写入第%d条数据' % suc)
            except Exception as e:
                error += 1
                print(e)
                pass

            f.close()
        except Exception as e:
            error += 1
            print(e)
            print("数据连接出现问题休息十分钟")
            time.sleep(600)
            pass
    print(f"成功输入{suc:d}")
    print(f"失败输入{error:d}")


def get_zwxx():
    all_urls = []
    f = open('zwxx_all_url.csv', 'r')
    reader = csv.reader(f)
    for i in reader:
        all_urls.append(i)
    f.close()

    f = open('zwxx.csv', 'a', newline='')
    writer = csv.writer(f)
    writer.writerow(['职位', '公司', '工资', '地点', '经验', '学历', '职位性质'])
    f.close()

    suc = 0
    error = 0
    for url in all_urls:
        try:
            f = open('zwxx.csv', 'a', newline='')
            writer = csv.writer(f)
            time.sleep(5)
            html = requests.get(url[0], headers=headers).text
            soup = BeautifulSoup(html, 'lxml')
            zwxx_lists = soup.find(class_='position-content-l')
            gs_lists = soup.find(class_='company')
            gs_lists = str(gs_lists)
            gs_lists = re.sub('<.*?>', '', gs_lists)
            gs_lists = re.sub('招聘$', '', gs_lists)
            # print(gs_lists)
            zwxx_lists = str(zwxx_lists)
            # print(zwxx_lists)
            pat = '<span.*?>(.*?)</span>'
            zw_list = re.findall(pat, zwxx_lists)
            # print(zw_list)
            try:
                zwxx_list = []
                for i in zw_list:
                    i = re.sub('/', '', i)
                    i = re.sub(' ', '', i)
                    zwxx_list.append(i)
                zwxx_list.insert(1, gs_lists)
                writer.writerow(zwxx_list)
                print(zwxx_list)
                suc += 1
                print('成功写入第%d条数据' % suc)
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
    print('成功输入%d' % suc)
    print('失败输入%d' % error)


if __name__ == '__main__':
    get_work_url()
    get_page_url()
    get_zw_url()
    get_zwxx()
