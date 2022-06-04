from gtts import gTTS
from db import *

word_data = fetchall('words',['word'])

def generate_audio(word: str):
    s = gTTS(word)
    s.save(f'audio/{word}.mp3')

for i in word_data:
    generate_audio(i['word'])