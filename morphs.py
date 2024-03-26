import json
from pymorphy2 import MorphAnalyzer
from rusyll import rusyll
morph = MorphAnalyzer()
rhymes = {}

# достаем для слова часть речи и сохраняем в словарь
# также я сначала думала делить слова на слоги, чтобы сделать ритмику с ударением, но ударение не получилось, а деление на слоги было убирать лень
with open('verses.json', 'r', encoding='utf-8') as f:
    verses = json.load(f)
    for title in verses:
        for line in verses[title]:
            word = line[0]
            ana = morph.parse(word)[0]
            pos = ana.tag.POS
            syllables = rusyll.word_to_syllables_wd(word)
            rhymes[word] = (pos, syllables)
# сохраняем словарь в джисоновский файл
with open('morphs.json', 'w', encoding='utf-8') as f:
  json.dump(rhymes, f, ensure_ascii = False)
