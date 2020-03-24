#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time    : 2020/3/22 上午 10:49
# @Email   : pasalai@qq.com
# @Github  : github.com/laishouchao
# @File    : tool.py
# @Software: PyCharm

import requests
import sys
import easygui as ui
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
        ui.msgbox(msg=base_info.replace(" ", "").replace("\n", ""), title="网站" + self.web_site + "扫描结果")
        # print("[√]完成：" + base_info)

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
            # ui.textbox(msg="网站" + website + "同IP网站的详细信息", title="网站" + website + "同IP网站的详细信息", text=tips)
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
        output = open('data.txt', 'w', encoding='gbk')
        output.write('url,status,title,cms,huanjing\n')
        for row in all_info:
            rowtxt = '{},{},{},{}'.format(row[0], row[1], row[2], row[3])
            output.write(rowtxt + "\n")
        output.close()
        with open("data.txt", encoding="gbk") as rp:
            text = rp.read()
        ui.textbox(msg="网站" + website + "同IP网站的详细信息", title="网站" + website + "同IP网站的详细信息", text=text)
        weizhi = ui.filesavebox(msg="表格保存", title="表格保存", default="./" + website + "结果.xls", filetypes="xls")
        print("[!]正在保存结果至" + website + "结果.xls")
        data_pd = pd.DataFrame(data=all_info, columns=["url", "状态值", "网站标题", "可能的CMS", "网站环境(包括中间件、开发框架、语言等信息)"])
        try:
            data_pd.to_excel(weizhi)
        except IOError:
            ui.msgbox("[x]保存失败，请检查是否已经打开该文件，或本程序是否有本文件夹及文件的读写权限")
            print("[x]保存失败，请检查是否已经打开该文件，或本程序是否有本文件夹及文件的读写权限")
        else:
            ui.msgbox("[√]保存成功！")
            print("[√]保存成功")


# 临时代码测试

# main()
if __name__ == '__main__':

    if ui.ccbox(msg="本软件仅供测试使用，对使用过程中造成的一切后果，作者不承担任何责任。", title="免责声明", choices=["同意承担使用本软件造成的一切责任", "算了吧，退出"]):
        website = ui.enterbox(msg="请输入网址，如:www.sdyunet.cn", title="同IP网站信息检测", default="www.sdyunet.cn")
        # print(website)
        all_info = []
        # website = input("[!]请输入网址，如www.site.com：\n")
        do_somthing_init = do_somting(web_site=website)
        do_somthing_init.getinfo()
        do_somthing_init.get_table()
        do_somthing_init.page_num()
        do_somthing_init.savexls()
    else:
        sys.exit(0)
