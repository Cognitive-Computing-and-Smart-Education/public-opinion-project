import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
import re

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
    doc_title = re.findall(r'<h1 class="post_title">(.*?)</h1>',doc_html)
    doc_info = re.findall(r'<div class="post_info">(.*?)</a>',doc_html)
    doc_text = re.findall(r'<div class="post_body">(.*?)<!-- AD200x300_1 -->')
    return  doc_html


if __name__ == '__main__':
    text = get_page()
    title,docurl = parse_page(text)
    doc_text = get_article_page(docurl[0])
    print(doc_text)
