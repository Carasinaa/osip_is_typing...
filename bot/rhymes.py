import json
from pymorphy2 import MorphAnalyzer
from rusyll import rusyll
import re
import random
morph = MorphAnalyzer()

vowels = ["а", "е", "ё", "и", "о", "у", "ы", "э", "ю", "я"]
pairs = [['б', 'п'], ['в', 'ф'], ['г', 'к'], ['з', 'с'], ['д', 'т'], ['ж', 'ш']]
suitable_words = []
with open('morphs.json', 'r', encoding='utf-8') as f:
    morphs = json.load(f)
with open('verses.json', 'r', encoding='utf-8') as f:
    verses = json.load(f)


def check_pair(l_1, l_2):
    for p in pairs:
        if l_1 in p and l_2 in p:
            return 'True'


def rhymes(word_1, word_2):
    if len(word_1) == 2 and len(word_2) == 2:
        if check_pair(word_1[-1], word_2[-1]) == 'True':
            if (word_1[-2] and word_2[-2] in vowels) and word_1[-2] == word_2[-2]:
                return 'True'
        if word_1[-1] == word_2[-1] and (word_1[-1] and word_2[-1] in vowels):
            if word_1[-2] == word_2[-2]:
                return 'True'
    if len(word_1) == 3 and len(word_2) == 3:
        if check_pair(word_1[-1], word_2[-1]) == 'True':
            if word_1[-2] == word_2[-2]:
                if word_1[-2] and word_2[-2] in vowels:
                    return 'True'
                else:
                    if word_1[-3] == word_2[-3]:
                        return 'True'
        if word_1[-1] == word_2[-1]:
            if word_1[-2] == word_2[-2]:
                if word_1[-3] != word_1[-3]:
                    return 'True'
    if len(word_1) == 1 or len(word_2) == 1:
        if word_1[-1] == word_2[-1]:
            return 'True'
    if len(word_1) == 2 or len(word_2) == 2:
        if check_pair(word_1[-1], word_2[-1]) == 'True':
            if word_1[-2] == word_2[-2]:
                return 'True'
        if word_1[-2:] == word_2[-2:]:
            return 'True'
    else:
        if word_1[-2:] == word_2[-2:]:
            if word_1[-1] and word_2[-1] not in vowels:
                if word_1[-2] and word_1[-2] not in vowels:
                    if word_1[-3] == word_2[-3]:
                        return 'True'
                else:
                    return 'True'
            else:
                if word_1[-2] == word_2[-2]:
                    return 'True'
        if check_pair(word_1[-1], word_2[-1]) == 'True':
            if word_1[-2] == word_2[-2]:
                if word_1[-2] and word_2[-2] in vowels:
                    return 'True'
                else:
                    if word_1[-3] == word_2[-3]:
                        return 'True'


def findrhyme(sentence):
    words = re.sub(r'[^\w\s]', '', sentence).split()
    last_word = words[-1]
    ana = morph.parse(last_word)[0]
    pos = ana.tag.POS

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
    if len(suitable_words) == 0:
        return 'Я не нашел рифму, попробуйте другое предложение, пожалуйста!'
    else:
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
        return f'{sentence}\n{random_sentence}\n\nИз "{title}"'

