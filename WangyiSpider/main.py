# encoding: utf-8
# Author    : 1476776320@qq.com
# Datetime  : 2021/07/27 9:24
# User      : TianXin
# Product   : PyCharm
# Project   : WangyiSpider
# File      : main.py
# Explain   : 备注


import requests
import re
import tools
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from lxml import etree

def get_url():
    page = ['','_02','_03','_04','_05','_06','_07','_08','_09','_10']
    doc_url = []
    for page in page:
        page_url = 'https://edu.163.com/special/002987KB/newsdata_edu_hot'+page+'.js?callback=data_callback'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        # 忽略requests证书警告
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(page_url,headers=headers,verify=False)
        title_url = re.findall(r'\"docurl\":\"(.*?)\"', response.text)
        doc_url += title_url
    return  doc_url

def get_article_page(doc_url):
    for i in range(len(doc_url)):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(doc_url[i], headers=headers, verify=False)
        doc_html = response.text
        doc_xml = etree.HTML(doc_html)
        try:
            title_id = re.findall(r'article/(.*?)\.html',doc_url[i])[0]
            doc_title = doc_xml.xpath('//h1[@class="post_title"]/text()')[0]
            doc_info = str(doc_xml.xpath('//div[@class="post_info"]/text()')[0]).replace(" ","")
            upload_time = re.findall(r'\s(.*?)\u3000', doc_info)
            upload_time = upload_time[0][0:10] + " " + upload_time[0][10:18]
            source = re.findall(r'(?<=来源:).*$',doc_info)[0]
            doc_content = doc_xml.xpath('//div[@class="post_body"]//*/text()')
            doc_text = ''
            for p in doc_content:
                doc_text += str(p)
            tools.save_data(title_id, doc_title, upload_time,source, doc_url[i], doc_text)
        except:
            print(doc_url[i])
        print(i)
    return  0


if __name__ == '__main__':
    doc_url = get_url()
    get_article_page(doc_url)
    print('\n\nfinished!')
