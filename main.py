import os
from colorama import init, Fore, Back, Style
import easyocr
import datetime
from PIL import Image, ImageGrab
import shutil

init(autoreset=True)
# 学生名单处理部分
print('正在处理学生名单...')
students = list()
raw_students = str()
with open('students.txt', 'r', encoding='utf-8') as f:
    raw_students = f.read()
    students = raw_students.split('\n')
# 学生独特字提取部分
output_students = dict()
no = 0
for student in students:

    list_to_write = list()
    list_to_write.append(student)
    for char in student:
        if char not in raw_students.replace(student, ''):
            list_to_write.append(char)
    if len(student) >= 3:
        for i in range(0, (len(student) // 2) + 1):
            if student[i: i + 2] not in raw_students.replace(student, ''):
                list_to_write.append(student[i: i + 2])
    no += 1
    if no <= 9:
        list_to_write.append('0'+str(no))
    else:
        list_to_write.append(str(no))
    output_students[student] = list_to_write
print(output_students)

# OCR部分
files_to_scan = str()
if str(input('是否自动从剪贴板中获取图片并识别？(y/n,default=Y)')) != 'n':
    shutil.rmtree('Screenshots')
    os.mkdir('Screenshots')
    while True:
        if str(input('按回车添加剪贴板现有图片...输入任意字符停止')) == '':
            try:
                path = os.path.join(os.getcwd(), 'Screenshots',
                                    str(datetime.datetime.now().timestamp()) + '.png')
                ImageGrab.grabclipboard().save(path)
                print(Fore.GREEN + "已经保存到 " + path)
            except AttributeError:
                print('剪贴板中没有图片，请重试！')
            continue
        else:
            break
files_to_scan = os.listdir('Screenshots')
reader = easyocr.Reader(['ch_sim'], gpu=True)  # need to run only once to load model into memory
ocr_results = str()
for f in files_to_scan:
    print(Fore.GREEN + 'Scanning ' + f + '...')
    result = reader.readtext(r"Screenshots/" + f, detail=0)
    for i in result:
        ocr_results += i
# 纠正非常常见的OCR识别错误
if '壬' not in raw_students:
    ocr_results = ocr_results.replace('壬', '王')
if '-' not in raw_students:
    ocr_results = ocr_results.replace('-', '一')
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
      " 共" + str(len(absent_students)) + "人缺席" + " 班级总人数" + str(len(output_students.keys())) + "\n缺席名单：",
      end='')
for student in absent_students:
    print(Fore.RED + student, end=' ')
print('\n')
