from gtts import gTTS
from db import *
import time


word_data = fetchall('words',['word'])
print(len(word_data))


def generate_audio(word: str):
    s = gTTS(word)
    s.save(f'audio/{word}.mp3')
    time.sleep(10)


for i in word_data:
    generate_audio(i['word'])

