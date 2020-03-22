#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time    : 2020/3/22 上午 10:49
# @Email   : pasalai@qq.com
# @Github  : github.com/laishouchao
# @File    : tool.py
# @Software: PyCharm

import requests
import pandas as pd
from lxml import etree


def requests_info(website):
    url = "http://dns.bugscaner.com/" + website + ".html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3941.4 Safari/537.36"}
    responses = requests.get(url=url, headers=headers).content.decode('utf-8')
    return responses

class do_somting():
    def __init__(self, web_site):
        # 发送请求初始化xpath
        self.web_site = web_site
        # self.all_info = []

    def getinfo(self):
        # 获取网址IP信息统计数据
        self.tree = etree.HTML(requests_info(self.web_site))
        base_info_1 = self.tree.xpath('//div/div[3]/div/text()')[0]
        base_info_2 = self.tree.xpath('//div/div[3]/div/strong/text()')
        base_info_3 = self.tree.xpath('//div/div[3]/div/text()')[1]
        base_info_4 = self.tree.xpath('//div/div[3]/div/span/text()')
        base_info_5 = self.tree.xpath('//div/div[3]/div/text()')[2]
        base_info = base_info_1 + str(base_info_2[0]) + base_info_3 + str(base_info_4[0]) + base_info_5
        print("[√]完成：" + base_info)

    def get_table(self):
        self.tree = etree.HTML(requests_info(self.web_site))
        # 获取详细信息
        tr_list = self.tree.xpath('//tbody/tr')

        for tr in tr_list:
            tips = []
            url = tr.xpath('td[2]/a/text()')
            tips.append(url[0])
            status = tr.xpath('td[3]/span/text()')
            tips.append(status[0])
            title = tr.xpath('td[4]/*/text()')
            tips.append(title[0])
            cms = tr.xpath('td[5]/text()')
            tips.append(cms[0])
            huanjing = tr.xpath("td[6]/text()")
            tips.append(huanjing[0])
            all_info.append(tips)
            print(tips)

    def page_num(self):
        # 获取返回数据的页数（直接通过总条数和显示条数计算获得)
        tips_num = self.tree.xpath('//div/div/span/text()')[0]
        pages = int(int(tips_num) / 15) + 2  # 15条每页，取整+1
        # print(pages)
        for page_num in range(2, pages):
            temp = self.web_site
            website = self.web_site + "_" + str(page_num)
            do_somthing_init = do_somting(web_site=website)
            do_somthing_init.get_table()
            self.web_site = temp

    def savexls(self):
        print("[!]正在保存结果至"+website+"结果.xls")
        data_pd = pd.DataFrame(data=all_info, columns=["url", "状态值", "网站标题", "可能的CMS", "网站环境(包括中间件、开发框架、语言等信息)"])
        try:
            data_pd.to_excel(website+"结果.xls")
        except IOError:
            print("[x]保存失败，请检查是否已经打开该文件，或本程序是否有本文件夹及文件的读写权限")
        else:
            print("[√]保存成功")



# 临时代码测试

# main()
if __name__ == '__main__':
    all_info = []
    website = input("[!]请输入网址，如www.site.com：\n")
    # website = "www.sdyunet.cn"  # 测试
    do_somthing_init = do_somting(web_site=website)
    do_somthing_init.getinfo()
    do_somthing_init.get_table()
    do_somthing_init.page_num()
    do_somthing_init.savexls()

