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


def qg_all_url():
    f = open('qg_all_url.csv', 'a', newline='')
    writer = csv.writer(f)

    url = 'http://www.51rc.com/'
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    suc = 0
    for i in soup.find_all(class_='Center'):
        url = str(i)
        pat = '<a href="(.*?)" target="_blank">.*?</a>'
        qg_url = re.findall(pat, url)
        for j in qg_url:
            urls = [j + '/newjob/j' + str(pn) for pn in (23, 24, 25, 26, 28)]
            for k in urls:
                l = [k]
                writer.writerow(l)
                suc += 1
                print(f"成功写入第{suc:d}条数据")

    f.close()


def get_page():
    qg_all_urls = []
    f = open('qg_all_url.csv', 'r')
    reader = csv.reader(f)
    for i in reader:
        qg_all_urls.append(i)
    f.close()
    suc = 0
    error = 0
    for url in qg_all_urls:
        f = open('zw_all_url.csv', 'a', newline='')
        writer = csv.writer(f)
        time.sleep(3)
        print(url)
        html = requests.get(url[0], headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        page = soup.find(class_='JobPageNum')
        # print(page)
        page = str(page)
        # print(page)
        pat = '第1/(.*?)页'
        page = re.findall(pat, page)
        try:
            if int(page[0]) >= 67:
                page = 68
            else:
                page = int(page[0]) + 1
            for i in range(1, page):
                zw_urls = []
                zw = url[0] + '_n' + str(i)
                zw_urls.append(zw)
                try:
                    writer.writerow(zw_urls)
                    suc += 1
                    print(f"成功写入第{suc:d}条数据")
                except Exception as e:
                    error += 1
                    print(e)
                    pass
        except Exception as e:
            error += 1
            print(e)
            pass
        f.close()


def get_zw():
    zw_all_urls = []
    f = open('zw_all_url.csv', 'r')
    reader = csv.reader(f)
    for i in reader:
        zw_all_urls.append(i)
    f.close()
    suc = 0
    error = 0
    for zw_url in zw_all_urls:
        f = open('zwxx_url.csv', 'a', newline='')
        writer = csv.writer(f)
        url = zw_url[0]
        URL = re.sub('/newjob/.*', '', url)
        html = requests.get(url, headers=headers).text
        time.sleep(2)
        # print(html)
        soup = BeautifulSoup(html, 'lxml')
        # print(soup)
        try:
            for items in soup.find_all(class_='JobName'):
                pat = str(items)
                # print(pat)
                pat1 = '<a class=".*?" href="(.*?)"'
                url_list = re.findall(pat1, pat)
                # print(url_list)
                for k in url_list:
                    # print(k)
                    zw_url_list = []
                    URl = str(URL) + str(k)
                    zw_url_list.append(URl)
                    # print(zw_url_list)
                    writer.writerow(zw_url_list)
                    suc += 1
                    time.sleep(1)
                    if int(int(time.clock()) % 100) == 0:
                        print('停止程序30秒')
                        time.sleep(30)
                    else:
                        print(zw_url)
                        print(f"第{suc:d}写入完毕")
        except Exception as e:
            error += 1
            print(e)
            print(f"第{error:d}条失败")
    f.close()
    print(f"共计成功{x:d}条")
    print(f"共计失败{y:d}条")


def get_zwxx():
    all_urls = []
    f = open('zwxx_url.csv', 'r')
    reader = csv.reader(f)
    for i in reader:
        all_urls.append(i)
    f.close()

    f = open('zwxx.csv', 'a', newline='')
    writer = csv.writer(f)
    writer.writerow(['职位', '公司', '地点', '工资', '招聘人数', '学历', '年龄要求', '工作经验', '招聘方式', '更新日期'])
    f.close()

    suc = 0
    error = 0
    for url in all_urls:
        try:
            zwxx_lists = []
            f = open('zwxx.csv', 'a', newline='')
            writer = csv.writer(f)
            print(url[0])
            html = requests.get(url[0], headers=headers).text
            soup = BeautifulSoup(html, 'lxml')
            zwlist = soup.find_all(class_='JobDetail')

            gsmc = soup.find(class_='DivCompany')
            gsmc = re.sub(' ', '', str(gsmc.a))
            gsmc = re.sub('<.*>', '', gsmc)
            gsmc = re.sub('\n', '', gsmc)
            gsmc = re.sub('\r', '', gsmc)

            zwxqlist = str(zwlist)
            zwxqlist = re.sub('\r', '', zwxqlist)
            zwxqlist = re.sub('\n', '', zwxqlist)
            pat = '<h2>(.*)</h2>'
            zwmc = re.findall(pat, zwxqlist)
            zwmc = zwmc[0]
            zwmc = re.sub(' ', '', zwmc)
            zwmc = re.sub('<.*>', '', zwmc)

            pat1 = '<a href=".*?" target=".*?">(.*?)</a>'
            gzdd = re.findall(pat1, zwxqlist)
            gzdd = gzdd[0]
            gzdd = re.sub(' ', '', gzdd)
            gzdd = re.sub('<.*>', '', gzdd)

            pat2 = '<span style=".*?">(.*?)</span>'
            gz = re.findall(pat2, zwxqlist)
            gz = gz[0]
            gz = re.sub(' ', '', gz)
            gz = re.sub('<.*>', '', gz)

            pat3 = '<td style="border-bottom: 1px dotted #E2E2E2;">(.*?)</td>'
            zp_list = re.findall(pat3, zwxqlist)
            zp_list = str(zp_list)
            zp_list = re.sub(' ', '', zp_list)
            zp_list = re.sub('<.*?>', '', zp_list)
            pat4 = '\'(.*?)\''
            zp_list = re.findall(pat4, zp_list)

            zwxx_lists.append(zwmc)
            zwxx_lists.append(gsmc)
            zwxx_lists.append(gzdd)
            zwxx_lists.append(gz)
            try:
                for i in zp_list:
                    i = re.sub('.*?：', '', i)
                    zwxx_lists.append(i)
                writer.writerow(zwxx_lists)
                print(zwxx_lists)
                suc += 1
                print(f"成功写入第{suc:d}条数据")
                f.close()
                time.sleep(5)
            except Exception as e:
                error += 1
                print(e)
                pass
        except Exception as e:
            error += 1
            print(e)
            print('数据连接出现问题休息十分钟')
            time.sleep(600)

    print(f"成功写入{suc:d}条数据")
    print(f"错误{error:d}条数据")


if __name__ == '__main__':
    qg_all_url()
    get_page()
    get_zw()
    get_zwxx()

