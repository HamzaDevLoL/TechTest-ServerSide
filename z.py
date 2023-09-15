
text = 'عبد الله عبد الرحن عبد الجبار'

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



print(temp)


