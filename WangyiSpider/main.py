import requests
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
from lxml import etree

def get_page():
    url = 'https://edu.163.com/special/002987KB/newsdata_edu_hot.js?callback=data_callback'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    # 忽略requests证书警告
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url,headers=headers,verify=False)
    text = response.text
    return  text

def parse_page(text):
    title = re.findall(r'\"title\":\"(.*?)\"',text)
    docurl = re.findall(r'\"docurl\":\"(.*?)\"',text)
    return title,docurl

def get_article_page(docurl):
    data=[]
    # for i in range(len(docurl)):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(docurl,headers=headers,verify=False)
    doc_html = response.text
    doc_xml = etree.HTML(doc_html)
    doc_title = doc_xml.xpath('//h1[@class="post_title]/text()')
    return  doc_title


if __name__ == '__main__':
    text = get_page()
    title,docurl = parse_page(text)
    doc_text = get_article_page(docurl[0])
    print(doc_text)
