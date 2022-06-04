from gtts import gTTS


def generate_audio(word: str):
    s = gTTS("word")
    s.save('audio/word.mp3')

