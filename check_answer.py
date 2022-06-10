from words import NewWord


class TrainingWord:
    def __init__(self, training_word: NewWord):
        self.training_word = training_word
        self.wrong_answer = 0

    def check_answer(self, answer: str):
        if answer == self.training_word.word:
            self.training_word.true_answer += 1
            self.training_word.answer_result = True
            return self.training_word
        else:
            self.wrong_answer += 1
            self.training_word

