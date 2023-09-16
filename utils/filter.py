import os
import re


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


def extractStudentInfo(text, pdfName):
    words = re.findall(r'\b\w+\b', text)[::-1]
    passing_grades = ["ناجح", "راسب"]
    writtenGrades = ['صفر', 'واحد', 'اثنان', 'ثلاث',
                     'اربع', 'خمس', 'ست', 'سبع', 'ثمان', 'تسع', 'عشر']
    name = ""
    result = ""
    grades = []
    for word in words:
        if word not in passing_grades and len(word) > 1 and all(char.isnumeric() for char in word) == False and word not in writtenGrades and all(x < len(word)-1 and (word[x] != 'غ' and word[x+1] != 'غ') for x in range(len(word))):
            if word == 'عبدا':
                name += 'عبد الله' + " "
            else:
                name += word + " "
        elif word in passing_grades:
            result = word
        elif any(word.find(grade) != -1 for grade in writtenGrades):
            tempList = []
            temp = ''
            for c in word:
                if c == 'غ':
                    tempList.append('غ')
                    word = word.replace('غ', '')
                elif c.isnumeric():

                    temp += c
                    word = word.replace(c, '')
                else:
                    if temp != '':
                        tempList.append(temp)
                        temp = ''
                    for i in range(len(writtenGrades)):
                        if word.find(writtenGrades[i]) != -1:
                            tempList.append(writtenGrades[i])
                            word = word.replace(writtenGrades[i], '')
            if temp != '':
                tempList.append(temp)
                temp = ''
            for i in range(len(tempList)):
                grades.append(tempList[i])
        else:

            if word == 'غ':
                grades.append('غ')
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
                    grades.append('غ')
            elif word.isnumeric():
                grades.append(word)
    print(text)
    json = {'name': name, 'StudientID': grades[10], "pdfName": pdfName, 'SequenceInPDF': grades[2],
            'Islamic': grades[11], 'Arbic': grades[9], 'English': grades[8], 'Biology': grades[7], 'math': grades[6], 'Chemistry': grades[5], 'Physics': grades[4], 'Sum': grades[3], 'result': result}

    return json
