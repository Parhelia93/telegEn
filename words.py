import db
from dataclasses import dataclass


@dataclass
class NewWord:
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
        self.train_limit = len(self.dataset)
        self.wrong_answer = 0

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
        self.wrong_answer = 0
        if self.counter < self.train_limit:
            word = self.dataset[self.counter]
            self.counter += 1
            return NewWord(word_id=word['word_id'], true_answer=word['true_answer'], false_answer=word['false_answer'],
                           stage=word['stage'], word=word['word'], word_translate=word['word_translate'],
                           answer_result=0)
        else:
            self.save_data_set()
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

    def get_train_limit(self):
        return self.train_limit

    def get_current_word(self):
        current_word = self.dataset[self.counter - 1]
        return NewWord(word_id=current_word['word_id'],true_answer=current_word['true_answer'],
                       false_answer=current_word['false_answer'],stage=current_word['stage'],word=current_word['word'],
                       word_translate=current_word['word_translate'],answer_result=0)

    def check_answer(self, answer: str):
        current_word = self.get_current_word()
        current_word_arr = current_word.word_translate.split(', ')

        if answer in current_word_arr and current_word.true_answer < 2:
            current_word.true_answer += 1
            self.save_word(current_word)
            new_word = self.get_new_word()
            return new_word
        elif answer in current_word_arr and current_word.true_answer >= 2:
            current_word.true_answer += 1
            self.save_word(current_word)
            current_word.answer_result = 1
            return current_word
        elif answer not in current_word_arr and self.wrong_answer < 2:
            self.wrong_answer += 1
            current_word.false_answer += 1
            current_word.answer_result = 2
            return current_word
        elif answer not in current_word_arr and self.wrong_answer >= 2:
            current_word.answer_result = 3
            current_word.false_answer += 1
            self.save_word(current_word)
            new_word = self.get_new_word()
            return new_word

    def check_user_choice(self, choice: str):
        user_choice = choice[-1]
        stage = 1 if user_choice == '1' else 0
        cur_word = self.get_current_word()
        cur_word.stage = stage
        self.save_word(cur_word)
        return self.get_new_word()