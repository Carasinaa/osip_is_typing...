import json
from pymorphy2 import MorphAnalyzer
from rusyll import rusyll
import re
import random
morph = MorphAnalyzer()

vowels = ["а", "е", "ё", "и", "о", "у", "ы", "э", "ю", "я"]
pairs = [['б', 'п'], ['в', 'ф'], ['г', 'к'], ['з', 'с'], ['д', 'т']]
suitable_words = []
with open('morphs.json', 'r', encoding='utf-8') as f:
    morphs = json.load(f)
with open('verses.json', 'r', encoding='utf-8') as f:
    verses = json.load(f)


def rhymes(last_syl_1, last_syl_2):
    if last_syl_1 == last_syl_2:
        return 'True'
    else:
        for p in pairs:
            if last_syl_1[-1] in p and last_syl_2[-1] in p:
                if last_syl_1[-2] in vowels and last_syl_2[-2] in vowels:
                    if len(last_syl_1) >= 3 and len(last_syl_2) >= 3:
                        if last_syl_1[-3] and last_syl_2[-3] not in vowels:
                            if last_syl_1[-2] == last_syl_2[-2]:
                                return 'True'
                        else:
                            if last_syl_1[-3] == last_syl_2[-3]:
                                return 'True'
                    else:
                        if last_syl_1[-2] == last_syl_2[-2]:
                            return 'True'


def findrhyme(sentence):
    words = re.sub(r'[^\w\s]', '', sentence).split()
    last_word = words[-1]
    syllabs = rusyll.word_to_syllables_wd(last_word)
    last_syl = syllabs[-1]
    ana = morph.parse(last_word)[0]
    pos = ana.tag.POS

    for m in morphs:
        pos_m = morphs[m][0]
        syllabs_m = morphs[m][1]
        last_syl_m = syllabs_m[-1]
        if pos == 'VERB':
            if pos_m != 'VERB' and m != last_word:
                if rhymes(last_syl_m, last_syl) == 'True':
                    suitable_words.append(m)
        elif pos == 'ADVB':
            if pos_m != 'ADVB' and m != last_word:
                if rhymes(last_syl_m, last_syl) == 'True':
                    suitable_words.append(m)
        else:
            if m != last_word:
                if rhymes(last_syl_m, last_syl) == 'True':
                    suitable_words.append(m)
    random_rhyme = random.choice(suitable_words)
    sentences = []
    for title in verses:
        for verse in verses[title]:
            if random_rhyme in verse:
                sentences.append((verse[1], title))
    random_line = random.choice(sentences)
    random_sentence = random_line[0]
    title = random_line[1]
    return f'{random_sentence}\n Из "{title}"'
