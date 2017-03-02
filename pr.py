#-*- coding: UTF-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import re
import os
import time
import xlwt


class seopy():

    def __init__(self):
        self.hosts_path="E:\TheWebSeo\mysite.txt"
        self.folder_path = "E:\TheWebSeo1"+ '\\' + str(
            time.strftime('%Y-%m-%d', time.localtime(time.time())))

    def request(self, url):  #封装的requests 请求
        r = requests.get(url)  # 像目标url地址发送get请求，返回一个response对象。有没有headers参数都可以。
        return r

    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print('创建名字叫做', path, '的文件夹')
            os.makedirs(path)
            print('创建成功！')
            return True
        else:
            print(path, '文件夹已经存在了，不再创建')
            return False


    def get_files(self, path): #获取文件夹中的文件名称列表
        pic_names = os.listdir(path)
        return pic_names

    def get_host(self,path):#逐行获取文件中的url
        a = open(path)
        lines = a.readlines()
        lists = []  # 直接用一个数组存起来就好了
        for line in lines:
            lists.append(line.split())
        return lists

    def get_data(self,paths):#抓取网页数据并放回数据结果
        path = "http://seo.chinaz.com/" + str(paths)
        print(path)
        print('数据开始采集！')
        driver = webdriver.PhantomJS()
        driver.get(path)
        html = driver.page_source  # 获取加载的网页内容
        soup = BeautifulSoup(html, 'lxml')
        data = [] # 声明一个空list用于存储获取数据

        data.append(paths)
        data.append(str(time.strftime('%Y-%m-%d', time.localtime(time.time()))))
        seo_itns = soup.select('div.SeoMaWr01Right > div')
        for each_list in seo_itns:
            if '权重' in str(each_list):
                p = '\d+'
                num_re = re.findall(p, str(each_list))
                data.append(str(num_re[-1]))
            elif 'Google' in str(each_list):
                p = '\d+'
                num_re = re.findall(p, str(each_list))
                data.append(str(num_re[-1]))
            else:
                data.append(str(each_list.get_text().split('：')[-1]))
        seo_bds = soup.select('ul.Manin01List01 > li.bbn > div.w10-7 ')
        for seo_bd in seo_bds:
            data.append(seo_bd.get_text())

        # data.append(str(soup.find(id='seo_BaiduPages').get_text()))
        # print(str(soup.find(id='seo_BaiduPages').get_text()))
        def get_id(id_name):
            id_value = soup.find(id=str(id_name))  # 获取特定id的文本
            # print(id_value.get_text())
            data.append(id_value.get_text())
        get_id('seo_BaiduPages')
        get_id('seo_GooglePages')
        get_id('seo_Pages360')
        get_id('seo_SogouPages')
        get_id('seo_BaiduLink')
        get_id('seo_GoogleLink')
        get_id('seo_Link360')
        return data

    def save_xls(self,data,url,num):
        xls_name = self.folder_path + '\\' + ''.join(url) + str(
            time.strftime('%Y-%m-%d', time.localtime(time.time()))) + '.xls'
        table_name = ''.join(url)+str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet(''.join(table_name), cell_overwrite_ok=True)
        for col in range(0, len(data)):
            sheet.write(col, num, ''.join(data[col]))


    def save_txt(self,data,url):
        folder_name = self.folder_path + '\\' + ''.join(url) + str(
            time.strftime('%Y-%m-%d', time.localtime(time.time()))) + '.txt'
        fobj = open(str(folder_name), 'w', encoding='utf-8')
        for col in range(0, len(data)):
            fobj.write( str(data[col]))
            fobj.write('\n')
        fobj.close()

    def spider(self):
        print('程序开始！')
        self.mkdir(self.folder_path )
        xls_name = self.folder_path + '\\' + str(time.strftime('%Y-%m-%d', time.localtime(time.time()))) + '.xls'
        table_name = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet(''.join(table_name), cell_overwrite_ok=True)
        data_head = ['网站名称', '查询时间', '整站世界排名', '整站流量排名', '整站日均IP', '150整站日均PV', '百度权重', '360权重', 'Google', '反链数',
                      '出站链接', '站内链接', '同IP网站', '响应时间', '备案号', '性质', 'IP', '域名年龄', '名称', '审核时间', '百度流量预计', '关键词库',
                      '百度快照', '首页位置', '索引量', '今日收录', '最近一周', '最近一月', '百度收录', '谷歌收录', '360收录', '搜狗收录', '百度反链', '谷歌反链',
                      '360反链']
        for num_head in range(0, len(data_head)):
            sheet.write( num_head, 0,''.join(data_head[num_head]))

        host_urls = self.get_host(self.hosts_path)
        for cols in range(0, len(host_urls)):
            host_url= host_urls[cols]
            data = self.get_data(''.join(host_url))
            self.save_txt(data,host_url)

            for cow in range(0, len(data)):
                sheet.write(cow, cols+1, ''.join(data[cow]))
        workbook.save(xls_name)
        print('程序结束！')


seo = seopy()
seo.spider()