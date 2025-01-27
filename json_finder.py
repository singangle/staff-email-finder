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

school_leaders = etree.HTML(response1.content).xpath('//*[@id="main-content"]/section[3]//td/p/text()')
school_leaders_email = etree.HTML(response1.content).xpath('//*[@id="main-content"]/section[3]//td/p/a/text()')
school_leaders_info = {}

for i in range(0, len(school_leaders), 3):
    school_leaders_info[school_leaders[i]] = [school_leaders[i+1], school_leaders_email[int(i/3)]]

print('Finished loading school leaders.')

# ----------------------------------------------------------------------------------------------------------------------

middle_managers = etree.HTML(response2.content).xpath('//*[@id="main-content"]/section[3]//tr/td/p/text()')
middle_managers_email = etree.HTML(response2.content).xpath('//*[@id="main-content"]/section[3]//tr/td/p/a/text()')
middle_managers_info = {}

removing_list = []

# for i in range(0, len(middle_managers), 3):
#     if middle_managers[i] == '\n' and middle_managers[i+1] == '\n' and middle_managers[i+2] == '\n':
#         removing_list.append(middle_managers[i])
#         removing_list.append(middle_managers[i+1])
#         removing_list.append(middle_managers[i+2])

# for num in removing_list:
#     middle_managers.remove(num)

# for i in range(0, len(middle_managers), 3):
#     if middle_managers[i] == '\n' and middle_managers[i+1] == '\n' and middle_managers[i+2] == '\n':
#         removing_list.append(middle_managers[i])
#         removing_list.append(middle_managers[i+1])
#         removing_list.append(middle_managers[i+2])

# middle_managers.remove('(Secondary 1 and 2)')
# # middle_managers.remove('(Secondary 3, 4 and 5)')

for i in range(0, len(middle_managers_email)):
    if middle_managers_email[i] == 'sitinorzahurin_sudin@moe.edu.sg' and middle_managers_email[i+1] == 'ong_yin_yin@moe.edu.sg':
        middle_managers_email.insert(i+1, '\n')

# for i in range(0, len(middle_managers), 3):
#     middle_managers_info[middle_managers[i]] = [middle_managers[i+1], middle_managers_email[int(i/3)]]
#     print(middle_managers_info[middle_managers[i]])

middle_managers.remove('(Secondary 1 and 2)')
middle_managers.remove('(Secondary 3, 4 and 5)')
middle_managers.remove('Email pending update')

while '\n' in middle_managers:
    middle_managers.remove('\n')

for i in range(0, len(middle_managers), 2):
    middle_managers_info[middle_managers[i]] = [middle_managers[i+1], middle_managers_email[int(i/2)]]


print('Finished loading middle managers.')

# ----------------------------------------------------------------------------------------------------------------------

teacher_leaders = etree.HTML(response3.content).xpath('//*[@id="main-content"]/section[3]//tr/td/p/text()')
teacher_leaders_email = etree.HTML(response3.content).xpath("//*[@id=\"main-content\"]/section[3]//tr/td/p/a/text()")
teacher_leaders_info = {}

while '\n' in teacher_leaders:
    teacher_leaders.remove('\n')

for i in range(0, len(teacher_leaders), 2):
    teacher_leaders_info[teacher_leaders[i]] = [teacher_leaders[i+1], teacher_leaders_email[int(i/2)]]

print('Finished loading teacher leaders.')

# ----------------------------------------------------------------------------------------------------------------------

form_teachers = etree.HTML(response4.content).xpath('//*[@id="main-content"]/section[3]//tr/td/p/strong/text() | //*[@id="main-content"]/section[3]//tr/td/p/text()')
form_teachers_email = etree.HTML(response4.content).xpath("//*[@id=\"main-content\"]/section[3]//tr/td/p/a/text()")
form_teachers_info = {}

while '\n' in form_teachers:
    form_teachers.remove('\n')

while '\xa0' in form_teachers:
    form_teachers.remove('\xa0')

for i in form_teachers_email:
    try:
        i = str(i)
    except:
        i = '\n'

form_teachers.remove('Class')
form_teachers.remove('Form Teachers')

print(form_teachers)
print(form_teachers_email)

name_count = 0
current_class = ''
for i in form_teachers:
    if i[0] == '1' or i[0] == '2' or i[0] == '3' or i[0] == '4' or i[0] == '5':
        current_class = i
        continue
    if i[0] != '1' and i[0] != '2' and i[0] != '3' and i[0] != '4' and i[0] != '5':
        form_teachers_info[current_class + " FT" +' ' + str(name_count)] = [i, form_teachers_email[name_count]]
        name_count -= -1

print(form_teachers_info)

# for i in range(0, len(form_teachers), 2):
#     form_teachers_info[form_teachers[i] + "FT"] = [form_teachers[i+1], form_teachers_email[int(i/2)]]

# print(form_teachers_info)

print('Finished loading form teachers.')

# ----------------------------------------------------------------------------------------------------------------------

all_teachers_info = {}
all_teachers_info.update(school_leaders_info)
all_teachers_info.update(middle_managers_info)
all_teachers_info.update(teacher_leaders_info)
all_teachers_info.update(form_teachers_info)

# check email addresses' legitimacy
for value in all_teachers_info.values():
    if re.match(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-"
                r"9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])", str(value[1])):
        continue
    else:
        value[1] = ''

print('Finished combining four dictionaries.')

# ----------------------------------------------------------------------------------------------------------------------

with open(r'C:\Users\hh415\Desktop\cs_projects\staff-email-finder\json\all_teachers_info.json', 'w') as f:
    json.dump(all_teachers_info, f, indent=4)

print('Finished updating json file.')

# ----------------------------------------------------------------------------------------------------------------------

current_time_struct = time.localtime()
formatted_time = time.strftime('%Y/%m/%d/%H:%M', current_time_struct)

with open(r'C:\Users\hh415\Desktop\cs_projects\staff-email-finder\json\timestamp.json', 'w') as t:
    json.dump(formatted_time, t, indent=4)

print("Finished updating timestamp")

# ----------------------------------------------------------------------------------------------------------------------

repo = git.Repo(r'C:\Users\hh415\Desktop\cs_projects\staff-email-finder')
repo.index.add(['json/all_teachers_info.json'])
repo.index.add(['json/timestamp.json'])

origin = repo.remotes.origin
origin.push()

print(f'\nUpdated name & email list. Timestamp: {formatted_time} Singapore time\n')