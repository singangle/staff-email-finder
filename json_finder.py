import git
import json
from lxml import etree
import requests
import re
import time

school_leaders_url = 'https://www.meridiansec.moe.edu.sg/about-us/our-organization/our-school-leaders/'
middle_managers_url = 'https://www.meridiansec.moe.edu.sg/about-us/our-organization/our-middle-managers/'
teacher_leaders_url = 'https://www.meridiansec.moe.edu.sg/about-us/our-organization/our-teacher-leaders/'
form_teachers_url = "https://www.meridiansec.moe.edu.sg/about-us/our-organization/our-form-teachers/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# responses
response1 = requests.get(school_leaders_url, headers=headers)
response2 = requests.get(middle_managers_url, headers=headers)
response3 = requests.get(teacher_leaders_url, headers=headers)
response4 = requests.get(form_teachers_url, headers=headers)

# ----------------------------------------------------------------------------------------------------------------------

school_leaders = etree.HTML(response1.content).xpath('//*[@id="main-content"]/section[3]//td/text()')
school_leaders_email = etree.HTML(response1.content).xpath('//*[@id="main-content"]/section[3]//td/a/text()')
school_leaders_info = {}

for i in range(0, len(school_leaders)):
    if i%2 == 0:
        school_leaders_info[school_leaders[i+1]] = [school_leaders[i], school_leaders_email[int(i/2)]]

print('Finished loading school leaders.')

# ----------------------------------------------------------------------------------------------------------------------

middle_managers = etree.HTML(response2.content).xpath('//*[@id="main-content"]/section[3]//tr/td/p/text()')
middle_managers_email = etree.HTML(response2.content).xpath('//*[@id="main-content"]/section[3]//tr/td/p/a/text()')
middle_managers_info = {}

for i in range(0, len(middle_managers)):
    if i%2 == 0:
        middle_managers_info[middle_managers[i+1]] = [middle_managers[i], middle_managers_email[int(i/2)]]

print('Finished loading middle managers.')

# ----------------------------------------------------------------------------------------------------------------------

teacher_leaders = etree.HTML(response3.content).xpath('//*[@id="main-content"]/section[3]//tr/td/p/text()')
teacher_leaders_email = etree.HTML(response3.content).xpath('//*[@id="main-content"]/section[3]//tr/td/p/a/text()')
teacher_leaders_info = {}

for i in range(0, len(teacher_leaders)):
    if i%2 == 0:
        teacher_leaders_info[teacher_leaders[i+1]] = [teacher_leaders[i], teacher_leaders_email[int(i/2)]]

print('Finished loading teacher leaders.')

# ----------------------------------------------------------------------------------------------------------------------

form_teachers = etree.HTML(response4.content).xpath('//*[@id="main-content"]/section[3]//tr/td/p/text()')
form_teachers_email = etree.HTML(response4.content).xpath("//*[@id=\"main-content\"]/section[3]//tr/td/p/a/text() |"
                                                          " //*[@id=\"main-content\"]/section[3]//tr/td/p/a/u/text() | "
                                                          "//tr/td[3][count(p/*)=0 and count(p/text())=0]")
form_teachers_info = {}

for i in form_teachers:
    if i == "\n":
        form_teachers.remove(i)

for i in range(0, len(form_teachers)):
    if i%2 == 0:
        form_teachers_info[form_teachers[i+1]] = [form_teachers[i] + " FT", form_teachers_email[int(i/2)]]

print('Finished loading form teachers.')

# ----------------------------------------------------------------------------------------------------------------------

all_teachers_info = {}
all_teachers_info.update(school_leaders_info)
all_teachers_info.update(middle_managers_info)
all_teachers_info.update(teacher_leaders_info)
all_teachers_info.update(form_teachers_info)

for value in all_teachers_info.values():
    if re.match(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-"
                r"9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])", str(value[1])):
        continue
    else:
        value[1] = ''

print('Finished combining four dictionaries.')

# ----------------------------------------------------------------------------------------------------------------------

with open('all_teachers_info.json', 'w') as f:
    json.dump(all_teachers_info, f, indent=4)

print('Finished updating json file.')

# ----------------------------------------------------------------------------------------------------------------------

current_time_struct = time.localtime()
formatted_time = time.strftime('%Y/%m/%d/%H:%M', current_time_struct)

# ----------------------------------------------------------------------------------------------------------------------

repo = git.Repo(r'C:\Users\hh415\Desktop\code\staff-email-finder')
repo.index.add(['all_teachers_info.json'])
repo.index.commit(f'Updated name & email list. Timestamp: {formatted_time} Singapore time')
print(f'\n Updated name & email list. Timestamp: {formatted_time} Singapore time')

origin = repo.remotes.origin
origin.push()
