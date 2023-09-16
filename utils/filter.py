import os
import re


def reversNames(text):
    words = text.split(" ")[::-1]

    temp = ''
    i = 0
    for x in range(len(words)):
        print(i)
        if i < len(words)-1 and words[i+1] == 'عبد':
            temp += words[i+1]+' '+words[i]+' '
            i += 2
        elif i < len(words):
            temp += words[i]+' '
            i += 1
    return temp


def textFilterToArray(text):
    start_index = text.index(': الفـــــرع')
    end_index = text.index('الحيائيالمعدل') + len('الحيائيالمعدل')
    while start_index != -1 and end_index != -1:
        text = text[:start_index] + text[end_index:]
        start_index = text.find(': الفـــــرع')
        end_index = text.find('الحيائيالمعدل') + len('الحيائيالمعدل')
    start_index = text.find('المركز مدير')
    while start_index != -1:
        end_index = start_index
        while end_index < len(text) and text[end_index] != '\n':
            end_index += 1
        text = text[:start_index] + text[end_index:]
        start_index = text.find('المركز مدير')
    start_index = text.find('المشاركون')
    end_index = len(text)
    text = text[:start_index] + text[end_index:]
    array = os.linesep.join(
        [line for line in text.splitlines() if line]).splitlines()
    return array


def extract_name_and_result(text, pdfName):
    words = re.findall(r'\b\w+\b', text)[::-1]
    passing_grades = ["ناجح", "راسب"]
    writtenGrades = ['صفر', 'واحد', 'اثنان', 'ثلاث',
                     'اربع', 'خمس', 'ست', 'سبع', 'ثمان', 'تسع', 'عشر']
    name = ""
    result = ""
    grades = []
    for word in words:
        if word not in passing_grades and len(word) > 1 and any(char.isnumeric() for char in word) == False and any(word.find(grade) == -1 for grade in writtenGrades):
            if word == 'عبدا':
                name += 'عبد الله' + " "
            else:
                name += word + " "
        elif word in passing_grades:
            result = word
        elif any(word.find(grade) != -1 for grade in writtenGrades):
            temp = []
            for grade in writtenGrades[::-1]:
                if word.find(grade) != -1:
                    temp.append(grade)
                    word = word.replace(grade, '')
            if (len(grades) > 0):
                grades.append(word)
            for i in temp:
                grades.append(i)
        else:
            if word == 'غ':
                grades.append('غ')
                print('==========1===========')

            elif any(char == 'غ' for char in word):
                temp = ''
                counter = 0
                for w in word:
                    if w == 'غ':
                        counter += 1
                    if w.isnumeric():
                        temp += w
                if (temp != ''):
                    grades.append(temp)
                for i in range(counter):
                    print(word)
                    grades.append('غ')
            elif word.isnumeric():
                grades.append(word)

    name = name.strip()
    json = {'name': name, 'StudientID': grades[10], "pdfName": pdfName, 'SequenceInPDF': grades[2],
            'Islamic': grades[11], 'Arbic': grades[9], 'English': grades[8], 'Biology': grades[7], 'math': grades[6], 'Chemistry': grades[5], 'Physics': grades[4], 'Sum': grades[3], 'result': result}

    return json
