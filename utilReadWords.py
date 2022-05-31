from db import *
result = []
with open("words.txt", "r") as file:
    for line in file:
            str1 = line.replace(']', '[')
            res = [a.replace('\t','').replace('\n','') for a in str1.split('[')]
            if len(res) == 3:
                result.append(res)
print(len(result))

for line in result:
    insert('words', {'word': line[0], 'word_transcription': line[1], 'word_translate': line[2], 'category_id':1})