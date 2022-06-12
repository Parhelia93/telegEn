import db
from typing import NamedTuple


class NewWord(NamedTuple):
    word_id: int
    true_answer: int
    false_answer: int
    stage: int
    word: str
    word_translate: str
    answer_result: int


class DataSet:
    def __init__(self, user_id: str, user_choice: str):
        self.limit = 10
        self.user_id = user_id
        self.user_choice = user_choice[-1]
        self.counter = 0
        self.dataset = self.get_user_dataset()

    def get_user_dataset(self):
        dataset = db.fetch_limit_and('users_words', ['word_id', 'true_answer', 'false_answer', 'stage'],
                                     'user_id', self.user_id, self.limit, 'stage', '0')
        for data in dataset:
            data_info = self.get_word_info(data['word_id'])
            data['word'] = data_info[0]['word'] if self.user_choice == '1' else data_info[0]['word_translate']
            data['word_translate'] = data_info[0]['word_translate'] if self.user_choice == '1' else data_info[0]['word']
        return dataset

    @staticmethod
    def get_word_info(word_id: str):
        return db.fetch_where('words', ['word', 'word_translate'], 'id', word_id)

    def get_new_word(self):
        if self.counter < self.limit:
            word = self.dataset[self.counter]
            self.counter += 1
            return NewWord(word_id=word['word_id'], true_answer=word['true_answer'], false_answer=word['false_answer'],
                           stage=word['stage'], word=word['word'], word_translate=word['word_translate'],
                           answer_result=0)
        else:
            return None

    def save_word(self, word_data: NewWord):
        word = self.dataset[self.counter-1]
        word['word_id'] = word_data.word_id
        word['true_answer'] = word_data.true_answer
        word['false_answer'] = word_data.false_answer
        word['stage'] = word_data.stage
        word['word'] = word_data.word
        word['word_translate'] = word_data.word_translate

    def save_data_set(self):
        for data in self.dataset:
            db.update_columnss('users_words', ['true_answer','false_answer','stage'],
                               [data['true_answer'],data['false_answer'],data['stage']], 'word_id', data['word_id'])

