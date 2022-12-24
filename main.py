import os
from colorama import init, Fore, Back, Style
import easyocr
import datetime

init(autoreset=True)

# 学生名单处理部分
students = list()
raw_students = str()
with open('students.txt', 'r', encoding='utf-8') as f:
    raw_students = f.read()
    students = raw_students.split('\n')
# 学生独特字提取部分
output_students = dict()
for student in students:
    list_to_write = list()
    list_to_write.append(student)
    for char in student:
        if char not in raw_students.replace(student, ''):
            list_to_write.append(char)
    output_students[student] = list_to_write
print(output_students)

# OCR部分
reader = easyocr.Reader(['ch_sim'], gpu=True)  # need to run only once to load model into memory
files_to_scan = os.listdir('Screenshots')
ocr_results = str()
for f in files_to_scan:
    print(Fore.GREEN + 'Scanning ' + f + '...')
    result = reader.readtext(r"Screenshots/" + f, detail=0)
    for i in result:
        ocr_results += i
print(Fore.WHITE + ocr_results)

# 检查部分
absent_students = list()
for student in output_students.keys():
    exist = False
    char_to_find = output_students[student]
    for char in char_to_find:
        if char in ocr_results:
            exist = True
            break
    if not exist:
        absent_students.append(student)

# 输出部分
print(Fore.RED + "统计自" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M') +
      " 共" + str(len(absent_students)) + "人缺席"+" 班级总人数"+str(len(output_students.keys()))+"\n缺席名单：", end='')
for student in absent_students:
    print(Fore.RED + student, end=' ')
