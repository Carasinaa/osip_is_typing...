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


def syls(syl_1, syl_2):
    if len(syl_1) >= 2 and len(syl_2) >= 2:
        if syl_1[-1] and syl_2[-1] in vowels and syl_1[-1] == syl_2[-1]:
            if syl_1[-2] == syl_2[-2]:
                return 'True'
        if check_pair(syl_1[-1], syl_2[-1]) == 'True':
            if syl_1[-2] and syl_2[-2] in vowels and syl_1[-2] == syl_2[-2]:
                return 'True'
    else:
        return 'False'


def rhymes(last_syl_1, num_syl_1, last_syl_2, num_syl_2):
    if num_syl_1 == 1 and num_syl_2 == 1:
        if last_syl_1 != last_syl_2:
            if syls(last_syl_1, last_syl_2) == 'True':
                return 'True'
    else:
        if last_syl_1 == last_syl_2:
            return 'True'
        if syls(last_syl_1, last_syl_2) == 'True':
            return 'True'


def findrhyme(sentence):
    words = re.sub(r'[^\w\s]', '', sentence).split()
    last_word = words[-1]
    syllabs = rusyll.word_to_syllables_wd(last_word)
    last_syl = syllabs[-1]
    ana = morph.parse(last_word)[0]
    pos = ana.tag.POS
    num_syl = len(syllabs)

    for m in morphs:
        pos_m = morphs[m][0]
        num_syl_m = len(morphs[m][1])
        syllabs_m = morphs[m][1]
        last_syl_m = syllabs_m[-1]
        if pos == 'VERB':
            if pos_m != 'VERB' and m != last_word:
                if rhymes(last_syl, num_syl, last_syl_m, num_syl_m) == 'True':
                    suitable_words.append(m)
        elif pos == 'ADVB':
            if pos_m != 'ADVB' and m != last_word:
                if rhymes(last_syl, num_syl, last_syl_m, num_syl_m) == 'True':
                    suitable_words.append(m)
        else:
            if m != last_word:
                if rhymes(last_syl, num_syl, last_syl_m, num_syl_m) == 'True':
                    suitable_words.append(m)
    if len(suitable_words) == 0:
        return 'Я не нашел рифму, попробуйте другое предложение, пожалуйста!'
    else:
        random_rhyme = random.choice(suitable_words)
        sentences = []
        for title in verses:
            for verse in verses[title]:
                if random_rhyme in verse:
                    sentences.append((verse[1], title))
        random_line = random.choice(sentences)
        random_sentence = random_line[0]
        title = random_line[1]
        return f'{random_sentence}\nИз "{title}"'

