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


def extractGrades(list, writtenGrades):
    result = []
    if 'غش' in list:
        result = ['غش', 'غش', 'غش', 'غش', 'غش',
                  'غش', 'غش']
        for word in list:
            if 'غش' in word:
                list.remove(word)
        return (result, list)
    tempWords = []

    for word in list:
        tempList = []
        temp = ''
        if 'غ' in word and all(word.find(grade) == -1 for grade in writtenGrades) and len(word) < 12:
            tempWords.append(word)

            for i in range(len(word)):
                if word[i] == 'غ':
                    tempList.append('غ')
                elif word[i].isnumeric():
                    temp += word[i]
                    if (i+1 < len(word) and not word[i + 1].isnumeric()) or i == len(word) - 1:
                        tempList.append(temp)

                        temp = ''
            for item in tempList:
                word = word.replace(item, '')
                result.append(item)
            if len(word) > 0:
                del result[len(result)-1]
                del tempWords[len(tempWords)-1]

        elif all(char.isnumeric() or char == '%' for char in word) and len(word) < 12:
            result.append(word.replace('%', ''))
            tempWords.append(word)

        elif any(word.find(grade) != -1 for grade in writtenGrades) and len(word) < 12:
            tempWords.append(word)

            indexesOfWrittenGrades = []
            for i in range(len(writtenGrades)):
                if word.find(writtenGrades[i]) != -1:
                    indexesOfWrittenGrades.append((word.find(writtenGrades[i]), word.find(
                        writtenGrades[i]) + len(writtenGrades[i]))
                    )
            indexesOfWrittenGrades.sort()
            tempList = []
            temp = ''
            for i in range(len(word)):
                if len(indexesOfWrittenGrades) > 0 and i == indexesOfWrittenGrades[0][0]:
                    tempList.append(word[i:indexesOfWrittenGrades[0][1]])
                    del indexesOfWrittenGrades[0]
                else:
                    if word[i] == 'غ':
                        tempList.append('غ')
                    elif word[i].isnumeric():
                        temp += word[i]
                        if (i+1 < len(word) and not word[i + 1].isnumeric()) or i == len(word) - 1:
                            tempList.append(temp)
                            temp = ''
            for item in tempList:
                word = word.replace(item, '')
                result.append(item)
            if len(word) > 0:
                del result[len(result)-1]
                del tempWords[len(tempWords)-1]

    if len(result) > 7:
        temp = result
        result = temp[0:6]
        result.append(temp[len(temp)-1])
    for item in tempWords:
        list.remove(item)
    return (result, list)


def extractStudentInfo(text, pdfName):
    writtenGrades = ['صفر', 'واحد', 'اثنان', 'ثلاث',
                     'اربع', 'خمس', 'ست', 'سبع', 'ثمان', 'تسع', 'عشر']
    words = (re.findall(r'\b\w+\b', text)[::-1])
    del words[0:2]
    result = words[1]
    words.remove(result)
    Sum = words[1]
    SequenceInPDF = words[0]
    del words[0:2]
    temp = extractGrades(words, writtenGrades)
    grades = temp[0]
    ID = temp[1][len(temp[1])-1]
    temp[1].remove(ID)
    name = ' '.join(temp[1]).replace('عبدا', 'عبدالله')
    json = {'name': name, 'StudientID': ID, "pdfName": pdfName, 'SequenceInPDF': SequenceInPDF,
            'Islamic': grades[0], 'Arbic': grades[1], 'English': grades[2], 'Biology': grades[3], 'math': grades[4], 'Chemistry': grades[5], 'Physics': grades[6], 'Sum': Sum, 'result': result}
    return json
