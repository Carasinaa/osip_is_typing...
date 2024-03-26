import json
from pymorphy2 import MorphAnalyzer
from rusyll import rusyll
import re
import random
morph = MorphAnalyzer()

# устанавливаем списки гласных и список пар для оглушения на конце слова
vowels = ["а", "е", "ё", "и", "о", "у", "ы", "э", "ю", "я"]
pairs = [['б', 'п'], ['в', 'ф'], ['г', 'к'], ['з', 'с'], ['д', 'т'], ['ж', 'ш']]
suitable_words = []
with open('morphs.json', 'r', encoding='utf-8') as f:
    morphs = json.load(f)
with open('verses.json', 'r', encoding='utf-8') as f:
    verses = json.load(f)


# функция для проверки пар глухости-звонкости
def check_pair(l_1, l_2):
    for p in pairs:
        if l_1 in p and l_2 in p:
            return 'True'


# по двум или трем последним буквам смотрим, "рифмуются" ли слова
# ударение осуществитеь не получилось, поэтому просто смотрим совпадение слов
def rhymes(word_1, word_2):
    # для двух двухбуквенных слов смотрим совпадение гласной и то, что последняя буква имеет пару по глухости звонкости
    if len(word_1) == 2 and len(word_2) == 2:
        if check_pair(word_1[-1], word_2[-1]) == 'True':
            if (word_1[-2] and word_2[-2] in vowels) and word_1[-2] == word_2[-2]:
                return 'True'
        if word_1[-1] == word_2[-1] and (word_1[-1] and word_2[-1] in vowels):
            if word_1[-2] == word_2[-2]:
                return 'True'
    # для трехбуквенных слов смотрим первую и вторую буквы на совпадение гласной/пару глухой/звонкий согласный
    if len(word_1) == 3 and len(word_2) == 3:
        # если слова заканчиваются на буквы из пары глухой/звонкий проверяем на совпадение второй и третьей буквы
        if check_pair(word_1[-1], word_2[-1]) == 'True':
            if word_1[-2] == word_2[-2]:
                if word_1[-2] and word_2[-2] in vowels:
                    return 'True'
                else:
                    if word_1[-3] == word_2[-3]:
                        return 'True'
        # если последняя буква одинаковая, то проверяем на одинаковую вторую и различающуюся третью
        if word_1[-1] == word_2[-1]:
            if word_1[-2] == word_2[-2]:
                if word_1[-3] != word_1[-3]:
                    return 'True'
    # если одно из слов однобуквенное, то достаточно просто совпадения последней буквы
    if len(word_1) == 1 or len(word_2) == 1:
        if word_1[-1] == word_2[-1]:
            return 'True'
    # если одно из слов двухбуквенное, то проверяем на пару глухости/звонкости, сопадающие гласные и согласные
    if len(word_1) == 2 or len(word_2) == 2:
        if check_pair(word_1[-1], word_2[-1]) == 'True':
            if word_1[-2] == word_2[-2]:
                return 'True'
        if word_1[-2:] == word_2[-2:]:
            return 'True'
    # если в обоих словах больше двух букв, проверяем совпадение последних двух букв
    else:
        if word_1[-2:] == word_2[-2:]:
            # если последняя и вторая с конца буква согласные, смотрим совпадение третьей буквы с конца
            if word_1[-1] and word_2[-1] not in vowels:
                if word_1[-2] and word_1[-2] not in vowels:
                    if word_1[-3] == word_2[-3]:
                        return 'True'
                else:
                    return 'True'
            else:
                if word_1[-2] == word_2[-2]:
                    return 'True'
        # если слова заканчиваются на пару глухости/звонкости, то смотрим совпадение гласной и последней согласной
        if check_pair(word_1[-1], word_2[-1]) == 'True':
            if word_1[-2] == word_2[-2]:
                if word_1[-2] and word_2[-2] in vowels:
                    return 'True'
                else:
                    if word_1[-3] == word_2[-3]:
                        return 'True'


# функция принимающая предложение и находящая "рифму"
def findrhyme(sentence):
    # принимаем предложение, отделяем последнее слово, смотрим часть речи
    words = re.sub(r'[^\w\s]', '', sentence).split()
    last_word = words[-1]
    ana = morph.parse(last_word)[0]
    pos = ana.tag.POS

    # подбираем все подходящие рифмующие слова, которые не совпадают по части речи с введенным слово, если это слово глагол или наречие
    # потому что рифмовать на глаголы и наречия не очень хорошо
    for m in morphs:
        pos_m = morphs[m][0]
        if pos == 'VERB':
            if pos_m != 'VERB' and m != last_word:
                if rhymes(last_word, m) == 'True':
                    suitable_words.append(m)
        elif pos == 'ADVB':
            if pos_m != 'ADVB' and m != last_word:
                if rhymes(last_word, m) == 'True':
                    suitable_words.append(m)
        else:
            if m != last_word:
                if rhymes(last_word, m) == 'True':
                    suitable_words.append(m)
    # подходящие слова, добавляем в список, если он пустой, говорим, что рифмы н нашли
    if len(suitable_words) == 0:
        return 'Я не нашел рифму, попробуйте другое предложение, пожалуйста!'
    else:
        # если слова нашли, то выбираем рандомное слово из списка, ищем все предложения с ним и выбираем также рандомное предложение
        random_rhyme = random.choice(suitable_words)
        suitable_words.clear()
        sentences = []
        for title in verses:
            for verse in verses[title]:
                if random_rhyme in verse:
                    sentences.append((verse[1], title))
        random_line = random.choice(sentences)
        sentences.clear()
        random_sentence = random_line[0]
        title = random_line[1]
        # ретерним предложение пользователя, найденное предложение и то, откуда она
        return f'{sentence}\n{random_sentence}\n\nИз "{title}"'

