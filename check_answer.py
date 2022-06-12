from words import NewWord


def check_answer(answer: str, training_word: NewWord):
    training_word = training_word
    word = training_word.word
    word_translate = training_word.word_translate
    true_answer = training_word.true_answer
    false_answer = training_word.false_answer
    answer_result = training_word.answer_result
    wrong_answer = 0
    word_translate_arr = training_word.word_translate.split(',')

    if answer in word_translate_arr and true_answer < 2:
        true_answer += 1
        answer_result = 1
    elif wrong_answer < 2 and answer != word_translate:
        wrong_answer += 1
        answer_result = 2
    elif answer in word_translate_arr and true_answer >= 2:
        true_answer += 1
        answer_result = 4
    else:
        wrong_answer += 1
        answer_result = 3
    return NewWord(word_id=training_word.word_id, true_answer=true_answer, false_answer=false_answer,
                   stage=training_word.stage, word=word, word_translate=word_translate,
                   answer_result=answer_result)

