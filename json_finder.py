import git
import json
from lxml import etree
import requests

school_leaders_url = 'https://www.meridiansec.moe.edu.sg/about-us/our-organization/our-school-leaders/'
middle_managers_url = 'https://www.meridiansec.moe.edu.sg/about-us/our-organization/our-middle-managers/'
teacher_leaders_url = 'https://www.meridiansec.moe.edu.sg/about-us/our-organization/our-teacher-leaders/'
form_teachers_url = "https://www.meridiansec.moe.edu.sg/about-us/our-organization/our-form-teachers/"

# 定义请求头部信息
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 发送 HTTP 请求并包含头部信息
response1 = requests.get(school_leaders_url, headers=headers)
response2 = requests.get(middle_managers_url, headers=headers)
response3 = requests.get(teacher_leaders_url, headers=headers)
response4 = requests.get(form_teachers_url, headers=headers)

school_leaders = etree.HTML(response1.content).xpath('//*[@id="main-content"]/section[3]//td/text()')
school_leaders_email = etree.HTML(response1.content).xpath('//*[@id="main-content"]/section[3]//td/a/text()')
school_leaders_info = {}

for i in range(0, len(school_leaders)):
    if i%2 == 0:
        school_leaders_info[school_leaders[i]] = [school_leaders[i+1], school_leaders_email[int(i/2)]]


print(school_leaders_info)