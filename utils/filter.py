import os

def reversNames(text):
    words = text.split(" ")[::-1]

    temp = ''
    i = 0
    for x in range(len(words)):
        print(i)
        if i < len(words)-1 and words[i+1] =='عبد':
            temp += words[i+1]+' '+words[i]+' '
            i += 2
        elif i < len(words):
            temp += words[i]+' '
            i+= 1
    return temp



def textFilterToArray(text):
    start_index = text.index(': الفـــــرع')
    end_index = text.index('الحيائيالمعدل') + len('الحيائيالمعدل')
    while start_index != -1 and end_index != -1:
        text = text[:start_index] + text[end_index:]
        start_index = text.find(': الفـــــرع')
        end_index = text.find('الحيائيالمعدل')+ len('الحيائيالمعدل')
    start_index = text.find('المركز مدير')
    while start_index != -1 :
        end_index = start_index 
        while end_index<len(text) and text[end_index] != '\n' :
            end_index += 1
        text = text[:start_index] + text[end_index:]
        start_index = text.find('المركز مدير')
    start_index = text.find('المشاركون')
    end_index = len(text)
    text = text[:start_index] + text[end_index:]
    array = os.linesep.join([line for line in text.splitlines() if line]).splitlines()
    return array






def extractStudentInfo(text,pdfName):
    temp = ''
    list = []
    for i in range(len(text)):
        
        if text[i].isnumeric():
            temp += text[i]
        elif text[i] == ' ' and temp.isnumeric() :
            list.append(temp)
            temp = ''
        elif text[i] == ' ' and i < len(text)-1 and text[i+1].isnumeric():
            list.append(temp)
            temp = ''
        elif text[i] == 'غ':
            temp = ''
            list.append('غ')
        else:
            temp += text[i]
    
    list[2] = reversNames(list[2])

    return {'name': list[2],'StudientID': list[1] ,"pdfName":pdfName,'SequenceInPDF':list[11] ,
            'Islamic':list[0],'Arbic':list[3],'English':list[4],'Biology':list[5],'math':list[6],'Chemistry':list[7] ,'Physics':list[8],'Sum':list[9] , 'result':list[10]}

