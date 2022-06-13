import db
from dataclasses import dataclass
import random


@dataclass
class NewWord:
    id: int
    word: str
    word_translate: str


class ShowDataSet:
    def __init__(self, user_id: str):
        self.limit = 10
        self.user_id = user_id
        self.counter = 0
        self.dataset = self.get_user_dataset()
        self.train_limit = len(self.dataset)

    def get_user_dataset(self):
        words = db.fetch_new_words_all('words', ['id', 'word', 'word_translate'], self.user_id, 1)
        data_set = random.sample(words, self.limit)
        return data_set

    def get_new_word(self):
        if self.counter < self.train_limit:
            word = self.dataset[self.counter]
            self.counter += 1
            return NewWord(id=word['id'], word=word['word'], word_translate=word['word_translate'])
        else:
            return None

    def user_choice(self, choice: str):
        code = choice[-1]
        current_word = self.dataset[self.counter-1]
        if code == '1':
            db.insert('users_words', {'word_id': current_word['id'], 'user_id': self.user_id, 'stage': 1})
        elif code == '2':
            db.insert('users_words', {'word_id': current_word['id'], 'user_id': self.user_id})
        return self.get_new_word()
